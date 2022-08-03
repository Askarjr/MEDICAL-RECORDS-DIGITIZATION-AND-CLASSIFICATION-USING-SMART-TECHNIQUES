const APP_ID='8965c2ff3d7c47e2be1d23e5a000273d'
const CHANNEL=sessionStorage.getItem('room')
const rtcToken=sessionStorage.getItem('rtcToken')
const rtmToken=sessionStorage.getItem('rtmToken')
let UID=sessionStorage.getItem('UID')
let NAME=sessionStorage.getItem('name')

let screenOn=false
let listOff=false
let vmute=false;
let amute=false;

let btnColor={false:'#fff',true:'#f77'}
let playerClass={false:'video-container',true:'hidden', video:'video-container', screen:'screen-container'}
let listClass={false:'usersList',true:'hidden'}
let zoomClass={false:'video-container',true:'fullScreen'}
let localTracks = []
let usersList=[]
let client=null

const userBoxPfx='user-container-'
const vidContainerPfx='video-streams'

//----------------------------------
// Remote Control
//-----------------------------------
const pointerPfx='pointer-'



function beginRemoteControl(hostId)
{
    sendMsg(`#AddPointer#,${hostId},${UID}`)
    createPointer(hostId,UID)
    let box=usersList[hostId].box
    box.addEventListener('mousemove',pointerMoved)
    box.addEventListener('ontouchmove',pointerMoved)
}

async function notifyUser(uid)
{
    await rtmClient.sendMessageToPeer({ text: '#BEGIN#' },uid)
    await rtmClient.sendMessageToPeer({ text: `#AddPointer#,${UID},${UID}` },uid)
}

async function pointerMoved(e)
{
    let w=this.clientWidth
    let h=this.clientHeight
    let x=event.offsetX
    let y=event.offsetY
    let hostId=this.dataset.uid
    //event.currentTarget.offsetX
    movePointer(hostId,UID,x,y,w,h)
    await sendMsg(`#MOVE#,${hostId},${UID},${x},${y},${w},${h}`)

}

function movePointer(hostId,guestId,x,y,gw,gh)
{
    let pointer=document.getElementById(`${pointerPfx}${hostId}-${guestId}`)
    let w=usersList[UID].box.clientWidth
    let h=usersList[UID].box.clientHeight

//    pointer.className='dot'
    let ws=w/gw
    let hs=h/gh
    let l=Math.round(x*ws)
    let t=Math.round(y*hs)
    pointer.style.left=l+'px'
    pointer.style.top=t+'px'
    console.debug(`${x} ${y}   ${ws} ${hs}    ${l} ${t}`)
}

function handleMessage(text,uid)
{
    let inf=text.split(',')
    switch(inf[0])
    {
        case '#AddPointer#': createPointer(inf[1],inf[2]); break;
        case '#MOVE#': movePointer(inf[1],inf[2],inf[3],inf[4],inf[5],inf[6]); break;
        case '#LEFT#':
    }
}
function createPointer(hostId,guestId)
{
    let name=usersList[guestId].name
 let pointer=`<div class='pointer' id="${pointerPfx}${hostId}-${guestId}"><span class="dot" ></span><span class="pointerName">${name}</span></div>`
 usersList[hostId].box.insertAdjacentHTML("afterbegin",pointer)
}

function removePointers(guestId)
{
     for (const [id, user] of Object.entries(usersList))
    {
        let pointer=document.getElementById(`${pointerPfx}${id}-${guestId}`)
        if(pointer!==undefined) pointer.remove()
    }

}

function removeLocalPointers()
{
     for (const [id, user] of Object.entries(usersList))
    {
        let pointer=document.getElementById(`${pointerPfx}${UID}-${id}`)
        if(pointer!==undefined&&pointer!=null) pointer.remove()
    }

}


////----------------------------------
// RTM
//----------------------------------

let rtmChannel=null
let rtmClient=null

function rtmMessage(msg, uid)
{
  switch(msg.text)
  {
      case '#BEGIN#': beginRemoteControl(uid); break;
      default: handleMessage(msg.text,uid);
  }
}

function rtmJoined(uid)
{
  //alert(`${uid} Joind RTM`)
}


function rtmLeft(guestId)
{
    removePointers(guestId)
}

async function joinRTM()
{
    rtmClient = AgoraRTM.createInstance(APP_ID)
	let options = {token: rtmToken, uid: UID}
    await rtmClient.login(options)
	rtmChannel= await rtmClient.createChannel(CHANNEL)
	await rtmChannel.join()
    rtmClient.on('MessageFromPeer', rtmMessage)
	rtmChannel.on('ChannelMessage',rtmMessage )
	rtmChannel.on('MemberJoined', rtmJoined)
	rtmChannel.on('MemberLeft', rtmLeft)
}

async function sendMsg(msgText)
{
    await rtmChannel.sendMessage({text:msgText})
}

//-------------------------------------
// join a channel and set client events
let join=async()=>{
    client= AgoraRTC.createClient({mode:'rtc', codec:'vp8'})
    client.on('user-joined',handleUserJoined)
    client.on("user-left", handleUserLeft);
    client.on('user-published',handleUserPublished)
    client.on('user-unpublished',handleUserUnpublished)
    client.on("user-info-updated",userInfoUpdated)
    addUser(UID)
    await client.join(APP_ID,CHANNEL,rtcToken,UID)
    displayLocalStream()
}

// add new user to usersList and add new hidden video-container
function addUser(uid,element=vidContainerPfx)
{
    let uname=uid.split('-')[0]
    let player= `<div class="hidden" id="${userBoxPfx}${uid}" data-uid="${uid}">
                <div class="username-wrapper" ondblclick="userDblClick()" data-uid="${uid}"><span class="user-name">${uname}</span></div>
               <div class="video-player" id="user-${uid}" ></div>
            </div>`
    document.getElementById(element).insertAdjacentHTML('beforeend', player)

    usersList[uid]={name:uname,amute:true,vmute:true,zoom:false}
    usersList[uid].box=document.getElementById(userBoxPfx+uid)
    if(screenOn) notifyUser(uid)
}

//
let playVideo=(uid,track=null)=>{
    if(track!=null) track.play(`user-${uid}`,{fit:'fill'})
    //playerClass[false]=screenOn? playerClass.screen : playerClass.video
    usersList[uid].box.className=playerClass[false]
    usersList[uid].box.style.cursor=screenOn? 'none' : ''
    updateUsersList(uid,{vmuted:false})
}

//
let playAudio=(uid,track=null)=>{
    if(track!=null) track.play()
    updateUsersList(uid,{amuted:false})
}

//
let stopVideo=(uid)=>{
    usersList[uid].box.className=playerClass[true]
    updateUsersList(uid,{vmuted:true})
}

//
let stopAudio=(uid)=>{
    updateUsersList(uid,{amuted:true})
}

//
let shareScreen=async()=>{
    screenOn=!screenOn
    event.target.style.backgroundColor=btnColor[screenOn]
    if(!screenOn){
        displayLocalStream()
        return;
    }

    await removeLocalStream();
    let screenTrack=await AgoraRTC.createScreenVideoTrack({encoderConfig: {framerate: 15,height: 720,width: 1280} },"auto")
    localTracks[0]=await AgoraRTC.createMicrophoneAudioTrack()
    if(screenTrack instanceof Array){
        localTracks[1] = screenTrack[0]
        localTracks[2] = screenTrack[1]
    }
    else{
        localTracks[1]  = screenTrack
    }

    playVideo(UID,localTracks[1])
    await client.publish(localTracks[1])
    await client.publish(localTracks[0])
    if(localTracks[2]!==undefined) await client.publish(localTracks[2]);
    sendMsg('#BEGIN#')
    beginRemoteControl(UID,UID)
}

//
let displayLocalStream= async ()=>{
	removeLocalPointers()
    await removeLocalStream()
    localTracks= await AgoraRTC.createMicrophoneAndCameraTracks()
    playVideo(UID,localTracks[1]);
    /*
    vmute=true;
    amute=true;
    await localTracks[1].setMuted(vmute)
    await localTracks[0].setMuted(amute)
    camBtn.style.backgroundColor=btnColor[amute]
    micBtn.style.backgroundColor=btnColor[vmute]
    */
    updateUsersList(UID,{amuted:amute})
    await client.publish([localTracks[0], localTracks[1]])
}
//--------------------------------------------
// AgoraRTC client events
//--------------------------------------------

// remote user joined the channel
let handleUserJoined=async(user)=>{
    addUser(user.uid)
}

// remote user left the channel
let handleUserLeft=async(user)=>{
    usersList[uid].box.remove()
    updateUsersList(user.uid,{del:true})
}

// remote user published new video or audio track
let handleUserPublished=async(user,mediaType)=>{
    await client.subscribe(user,mediaType)
    if(mediaType==='video') playVideo(user.uid,user.videoTrack)
    else playAudio(user.uid,user.audioTrack)
}

// remote user unpublished video or audio track
let handleUserUnpublished=async(user,mediaType)=>{
    await client.subscribe(user,mediaType)
    if(mediaType==='video') stopVideo(user.uid)
    else stopAudio(user.uid)
}

// remote user video or audio state changed
let userInfoUpdated=async(uid,msg)=>{
    switch(msg)
    {
        case 'mute-audio':  stopAudio(uid); break;
        case 'unmute-audio':playAudio(uid); break;
        case 'mute-video':  stopVideo(uid); break;
        case 'unmute-video':playVideo(uid); break;
    }
}

//-----------------------------------------
// helper functions and local events
//-----------------------------------------
function userDblClick()
{
    let uid=event.currentTarget.dataset.uid
    usersList[uid].zoom=!usersList[uid].zoom
    usersList[uid].box.className=usersList[uid].zoom? zoomClass[true] : zoomClass[false]

}
let removeLocalStream=async()=>{
    await client.unpublish(localTracks)
    for(let i=0; localTracks.length>i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    localTracks=[]
    resetButtons()
}

let leaveAndRemoveLocalStream=async()=>{
    await removeLocalStream()
    await client.leave()
    await rtmChannel.leave()
    window.open('/lobby','_self')
}

let resetButtons=()=>{
     camBtn.style.backgroundColor=btnColor[false]
     micBtn.style.backgroundColor=btnColor[false]
     vmute=false;
     amute=false;
}

let toggleCamera=async(e)=>{
    vmute=!vmute;
    e.target.style.backgroundColor=btnColor[vmute]
    await localTracks[1].setMuted(vmute)
    if(vmute) stopVideo(UID);
    else playVideo(UID);
}

let toggleMic=async(e)=>{
    amute=!amute;
    e.target.style.backgroundColor=btnColor[amute]
    await localTracks[0].setMuted(amute)
    updateUsersList(UID,{amuted:amute})
}

let toggleList=()=>{
    listOff=!listOff
    listBtn.style.backgroundColor=btnColor[listOff]
    ulist.className=listClass[listOff]
}

// update user and display updated list
let updateUsersList=(uid,inf)=>{
    if(inf.del!==undefined) delete usersList[uid]
    else usersList[uid]=Object.assign(usersList[uid],inf)
    let listHtml=''
    for (const [id, user] of Object.entries(usersList))
    {
        listHtml+=
            `<div class="user-wrapper">
                <span class="user-name">${user.name}</span>
                <img class="state-icon" style="background-color:${btnColor[user.amuted]};" src="/static/assets/images/video/microphone.svg"/>
                <img class="state-icon" style="background-color:${btnColor[user.vmuted]};" src="/static/assets/images/video/video.svg"/>
            </div>`
    }
    document.getElementById('usersList-wrapper').innerHTML=listHtml;
}

//-------------------------------------------------------------------
// startup code
//-------------------------------------------------------------------

// get document (html) elements
document.getElementById('room-name').innerText=CHANNEL
let leaveBtn=document.getElementById('leave-btn')
let camBtn=document.getElementById('camera-btn')
let micBtn=document.getElementById('mic-btn')
let scrBtn=document.getElementById('mic-btn')
let listBtn=document.getElementById('list-btn')
let ulist=document.getElementById('usersList-wrapper')

// set ui events
leaveBtn.addEventListener('click',leaveAndRemoveLocalStream)
camBtn.addEventListener('click',toggleCamera)
micBtn.addEventListener('click',toggleMic)

//hide users list and join the channel
toggleList()
join()
joinRTM()
