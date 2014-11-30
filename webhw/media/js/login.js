/**
 * Created with PyCharm.
 * User: vs
 * Date: 09.12.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */

$("#guest_login").click(function ()
{
    $("#id_user").val("anonymous")
    $("#id_password").val("password")
    $("#login_form").submit();
}
    );

$("#login").click(function ()
    {
        $("#login_form").submit();
    }
);
