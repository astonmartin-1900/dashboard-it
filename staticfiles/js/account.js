$( document ).ready(function() {
    $(".checkbox-dropdown").click(function () {
        var dropdown_elements_list = $(".facilitator_selector").find(".checkbox-dropdown")
        if ($(this).hasClass("is-active")){
            $(this).toggleClass("is-active");
        } else {
            for (let i=0; i<dropdown_elements_list.length; i++){
                dropdown_elements_list[i].classList.remove("is-active");
            }
            $(this).toggleClass("is-active");
        }
    });
    $(".checkbox-dropdown ul").click(function(e) {
        e.stopPropagation();
    });
    $(".selector_body_item").hover(
    function(){
        $(this).css("background-color", "#34220d40");
        $(this).children().css("background-color", "transparent");
    },function() {
        $(this).css("background-color", "transparent");
        $(this).children().css("background-color", "#F5F6F8");
        $(this).children(".wor_week").css("background-color", "transparent");
    }); 
    $(".wor_week").click(function (){
        var content = $(this).parent();
        var view_form = $(".facilitators");
        /////////// WEEK UPDATE ////////////////
        $(view_form).children(".page-title").html("The "+$(this).children().html()+" facilitators:");
        /////////// WOR LEADER /////////////////
        //view fields detection
        var wor_leader_image = view_form.find('.user_image')[0];
        var wor_leader_block = view_form.find(".user_description")[0];

        var wor_leader_user_information = $(wor_leader_block).children(".user_information_block").children('.user_information');
        var wor_leader_user_personal_data = $(wor_leader_block).children(".user_personal_data_block").children('.user_personal_data');
        //getting leader fileds value
        var wor_leader_current_image = $(content).children(".wor_leader").children(".user_profile").children(".user_image").html();
        var wor_leader_personal_data = $(content).children(".wor_leader").children(".user_profile").children(".user_information");
        //data updating
        var wor_leader_first_name = $(wor_leader_personal_data).children(".first_name").html();
        var wor_leader_last_name = $(wor_leader_personal_data).children(".last_name").html();
        var wor_leader_email = $(wor_leader_personal_data).children(".email").html();
        var wor_leader_position = $(wor_leader_personal_data).children(".position").html();
        
        $(wor_leader_image).html($(wor_leader_current_image));
        $(wor_leader_user_information).children(".user_name").html(wor_leader_first_name + " "+ wor_leader_last_name);
        $(wor_leader_user_information).children(".user_position").html(wor_leader_position);
        $(wor_leader_user_personal_data).children(".data").html(wor_leader_email);
        /////////// WOR ENGAGER /////////////////
        // view fields detection
        var wor_engager_image = view_form.find('.user_image')[1];
        var wor_engager_block = view_form.find(".user_description")[1];
        
        var wor_engager_user_information = $(wor_engager_block).children(".user_information_block").children('.user_information');
        var wor_engager_user_personal_data = $(wor_engager_block).children(".user_personal_data_block").children('.user_personal_data');
        //getting engager fileds value
        var wor_engager_current_image = $(content).children(".wor_engager").children(".user_profile").children(".user_image").html();
        var wor_engager_personal_data = $(content).children(".wor_engager").children(".user_profile").children(".user_information");
        //data updating
        var wor_engager_first_name = $(wor_engager_personal_data).children(".first_name").html();
        var wor_engager_last_name = $(wor_engager_personal_data).children(".last_name").html();
        var wor_engager_email = $(wor_engager_personal_data).children(".email").html();
        var wor_engager_position = $(wor_engager_personal_data).children(".position").html();

        $(wor_engager_image).html($(wor_engager_current_image));
        $(wor_engager_user_information).children(".user_name").html(wor_engager_first_name +" " + wor_engager_last_name);
        $(wor_engager_user_information).children(".user_position").html(wor_engager_position);
        $(wor_engager_user_personal_data).children(".data").html(wor_engager_email);

    });
});