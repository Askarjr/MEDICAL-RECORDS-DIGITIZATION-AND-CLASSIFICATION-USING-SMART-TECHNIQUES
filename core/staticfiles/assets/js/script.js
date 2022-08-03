$(document).ready(()=>{
    // ===================home page===============================================
    $(".close-icon").click(function(){
        $(".navbar-collapse").animate({right:'-100%'},200);
        $(".navbar-collapse").removeClass("show");
    })
    $(".navbar-toggler").click(function(){
        $(".navbar-collapse").animate({right:'0%'},200);
    })
    $(".nav-item").click(function(){
        $(this).toggleClass("click-drop")
    })
    // ============================sign-in page================================================
    $(".sign-form").animate({
        top:'187px'
    },500)
    $(".sign-form").animate({
        width:'520px'
    },500)
    $(".sign-form").animate({
        height:'359px'
    },500,function(){
        $("h2").slideDown(500,function(){
            $(".form-group").show(500,function(){
                $(".check-group").show(500,function(){
                    $(".forgetpass").show(500,function(){
                        $(".login").fadeIn(500)
                    })
                })
                
            })
        })
    })

    // -------------------ribbons animation
    $(".ribb1").animate({
        right: '156px'
    },500)
    $(".ribb2").animate({
    right: '-136px'
    },600)
    $('.ribb3').animate({
        right:'135px'
    },700)
    $('.ribb4').animate({
        right:'12px'
    },800)
    
})
// $(".check-group").show("slide",{direction:"left"},1000,function(){
//     $(".forgetpass").toggle("slide",{direction:"right"},1000)
// })
// $(".forgetpass").show("slide",{direction:"right"},1000)