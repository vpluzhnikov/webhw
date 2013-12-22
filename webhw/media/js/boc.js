/**
 * Created with PyCharm.
 * User: vs
 * Date: 09.12.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */
$("#load").click(function ()
    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
        $("#xls_file").click();
    }
);

$("#xls_file").change(function ()
{
    console.log($("#xls_file").val());
    $("#boc_form").submit();
}
);

$("#save").click(function ()
    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
        window.alert("save");
    }
);

//$("#add_req").click(function ()
//    {
//        var url_boc_xlssave = "/boc_xlssave"
//        gdata = {}
//        i = 1
//        for (line in griddata) {
//            gdata[i] = griddata[line];
//            i++;
//        }
//        $.ajax({
//            type : 'POST',
//            url: url_boc_xlssave,
//            async: false,
//            dataType: 'json',
//            data: {"json" : JSON.stringify(griddata) },
//            success: function(data, status){
//                error = data.error;
//                console.log(data);
//                element = '<input id="xlsfilename" name="xlsfilename" value="'+ data['filename'] +'" type="hidden">'
//                var input = $('#boc_form').appendTo(document.body).append(element);
//            }
//        });
//        window.alert("add");
//    }
//);

$('#add_req').click(function() {
    $('#add_req_dialog').arcticmodal();
});

$("#itemtype2").click(function() {
    if ($(this).val() == 'new'){
        $("#upgrade_params").fadeOut(300);
    } else {
        $("#upgrade_params").fadeIn(300);
    }

});

$("#itemtype1").click(function() {
    if ($("#itemtype2").val() == 'new') {
        if ($(this).val() == 'db') {
            $("#cpu_count").val('4');
            $("#ram_count").val('32');
            $("#hdd_count").val('300');
        }
        if ($(this).val() == 'app') {
            $("#cpu_count").val('6');
            $("#ram_count").val('48');
            $("#hdd_count").val('100');
        }
        if ($(this).val() == 'term') {
            $("#cpu_count").val('4');
            $("#ram_count").val('24');
            $("#hdd_count").val('100');
        }
        if ($(this).val() == 'lb') {
            $("#cpu_count").val('-');
            $("#ram_count").val('-');
            $("#hdd_count").val('-');
            $("#san_count").val('-');
            $("#nas_count").val('-');
        }
        if ($(this).val() == 'dp') {
            $("#cpu_count").val('-');
            $("#ram_count").val('-');
            $("#hdd_count").val('-');
            $("#san_count").val('-');
            $("#nas_count").val('-');
        }
    }
});
