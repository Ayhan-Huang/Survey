/**
 * Created by aibuz on 2017/11/2.
 */





function AddScore(ele) {
    //改样式
    console.log(ele);
    $(ele).parent().addClass("active");
    $(ele).parent().siblings().removeClass("active");
    $(ele).parent().parent().parent().parent().removeAttr("style");

}

function FormVerification() {
    //表单验证和数据提取
    var data_dic = {
        'username': $("#username").val() //调查问卷者的姓名
    };
    var err_flag = false;//set to true when some data is missing
    //console.log($("#survery_list").children(".bord-no"));
    $("div[answer_type='score']").each(function (index, ele) {
        // 循环所有的打分，找出打分和原因
        console.log($(ele).attr("question_id"));
        var selected_score = $(ele).find("li").filter(".active").text();
        var suggestion = $(ele).find("textarea").val();
        if (selected_score.length == 0) {
            $(ele).css("background", "orange");
            err_flag = true;
        } else {
            //add user selected score to data_dic for later posting
            data_dic[$(ele).attr("question_id")] = {
                "score": selected_score,
                "suggestion": suggestion,
                "single": '',
            };

        }
    });//end score verification

    $("div[answer_type='suggestion']").each(function (index, ele) {
        //找出所有建议
        var suggestion = $(ele).find("textarea").val();
        if (suggestion.length < 15) {
            $(ele).css("background", "orange");
            err_flag = true;
        } else {
            //add user selected score to data_dic for later posting
            data_dic[$(ele).attr("question_id")] = {
                "score": 0,
                "suggestion": suggestion,
                "single": '',
            };

            $(ele).removeAttr("style");
        }

    });//end suggestion verification


    $("div[answer_type='single']").each(function (index, ele) {
        //找出所有的单选
        var single = $(ele).find("label").filter('.active').find('input').val()
        if (!single) {
            $(ele).css("background", "orange");
            err_flag = true;
        } else {
            //add user selected score to data_dic for later posting
            data_dic[$(ele).attr("question_id")] = {
                "score": 0,
                "suggestion": '',
                "single": single
            };

            $(ele).removeAttr("style");
        }

    });//end suggestion verification

    return [err_flag, data_dic]
    //console.log(data_dic);
}//end FormVerification

$(document).ready(function () {


    $("button").click(function () {

        var result = FormVerification();
        if (result[0] == true) { //didn't pass the form verification
            alert("请回答完所有问题后再提交!");

        } else {
            console.log(result)
            console.log("--ready to submit---")
            var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
            var data = {
                'data': JSON.stringify(result[1]),
                'csrfmiddlewaretoken': csrftoken
            }

            $.post(window.location.href, data, function (callback) {

                console.log("callback;");
                console.log(callback);
                var res = JSON.parse(callback);
                $("#response_data").html(" ");

                $.each(res, function (key, item) {
                    var err_msg = "<p style='color:red;'>" + key + ": " + item + "</p>";
                    $("#response_data").append(err_msg);
                });//end each

                if ($("#response_data").children().length == 0) { // no err msg
                    console.log('----success submit--');
                    var info_msg = "<p style='color:green;'>感谢您的参与,我们会认真阅读您的建议并努力去改进!</p>";
                    $("#response_data").append(info_msg);
                }

                console.log("err length:" + res.length)
            });//end post
        }

    });//end button click


});//end document ready

