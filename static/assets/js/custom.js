jQuery(document).ready(function($) 
{
    //check all click event
    $('#check-all').click(function () 
    {
        if ($('#check-all').is(':checked') == true) 
        {
            $(".chk").prop('checked', true);
            $("#action_btn").show()
        }
        else
        {
            $(".chk").prop('checked', false);
            $("#action_btn").hide()
        }
    });
    //single check click event
    $('.chk').click(function() 
    {
        if($('.chk:checked').length == $('.chk').length)
        {
            $('#check-all').prop('checked', true);
            $("#action_btn").show()
        }
        else if($('.chk:checked').length == 0)
        {
            $("#action_btn").hide()
        } 
        else 
        {
            $('#check-all').prop('checked', false);
            $("#action_btn").show()
        }
    });


     //check all click event
     $('#id_check_all').click(function () 
     {
         if ($('#id_check_all').is(':checked') == true) 
         {
             $(".chk-days").prop('checked', true);
         }
         else
         {
             $(".chk-days").prop('checked', false);
         }
     });
     //single check click event
     $('.chk-days').click(function() 
     {
         if($('.chk:checked').length == $('.chk-days').length)
         {
             $('#id_check_all').prop('checked', true);
            
         }
         else if($('.chk-days:checked').length == 0)
         {
            $('#id_check_all').prop('checked', false);
         } 
         else 
         {
             $('#id_check_all').prop('checked', false);
         }
     });

    $('#id_state').on('change', function() 
    {
        $.ajax(
        {
            url: "/cities/"+this.value, 
            success: function(result)
            {
                $('#id_city').html(result)
            }
        });

    });

    $('#id_category').on('change', function() 
    {
        $.ajax(
        {
            url: "/subcategories/"+this.value, 
            success: function(result)
            {
                $('#id_subcategory').html(result)
            }
        });

    });

    var maxLength = 150;
    $('#id_comment').keyup(function() 
    {
        var textlen = maxLength - $(this).val().length;
        $('#rchars').text(textlen);
    });

    $("#blog_comment").submit(function (e) 
    {
        // preventing from page reload and default actions
        e.preventDefault();
        // serialize the data for sending the form data.
        var serializedData = $(this).serialize();
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "/blog/post_comment",
            data: serializedData,
            success: function (result) 
            {
                if(result.status == 'error')
                {
                    window.location = "/sign-in";
                }
                else
                {
                    $('#id_comment').val(''); 
                    $('#rchars').text(maxLength);
                    
                    $("#comment_section").html('');
                    $("#comment_section").html(result.data);
                    $("#comments-count").html('');
                    $("#comments-count").html(result.total_comments+' Comments');
                    $("#top_comments_count").html(result.total_comments+' Comments');
                    $("#comment_added").show();

                    if(result.has_next == '')
                    {
                        $("#loading-box").hide();
                    }
                    else
                    {
                        $("#loading-box").show();
                        $('#next_page_number').val(result.has_next)
                    }

                }
            },
            error: function (result) 
            {
                window.location = "/sign-in";
            }
        })
    })

    $("#load-btn").click(function (e) 
    {
        var blog                = $('#id_blog').val();
        var total_comments      = $('#total_comments').val();
        var total_comments_load = $('#total_comments_load').val();
        total_comments_load     = total_comments_load + 3
        var next_page_number = $('#next_page_number').val();
        $.ajax(
            {
            url: "/blog/comments/"+blog+"?page="+next_page_number, 
            success: function(result)
            {
                $("#comment_section").append(result.data);
                if(result.has_next == '')
                {
                    $("#loading-box").hide();
                }
                else
                {
                    $('#next_page_number').val(result.has_next)
                }
            }
        });

    })


    

    $('#tue_mon_copy').click(function () 
    {
        if ($('#tue_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()

            $('#id_tue_start_hr').val(mon_start_hr)
            $('#id_tue_start_ap').val(mon_start_ap)
            $('#id_tue_end_hr').val(mon_end_hr)
            $('#id_tue_end_ap').val(mon_end_ap)
        }
    });

    $('#wed_mon_copy').click(function () 
    {
        if ($('#wed_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()

            $('#id_wed_start_hr').val(mon_start_hr)
            $('#id_wed_start_ap').val(mon_start_ap)
            $('#id_wed_end_hr').val(mon_end_hr)
            $('#id_wed_end_ap').val(mon_end_ap)
        }
    });

    $('#thu_mon_copy').click(function () 
    {
        if ($('#thu_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()

            $('#id_thu_start_hr').val(mon_start_hr)
            $('#id_thu_start_ap').val(mon_start_ap)
            $('#id_thu_end_hr').val(mon_end_hr)
            $('#id_thu_end_ap').val(mon_end_ap)
        }
    });

    $('#fri_mon_copy').click(function () 
    {
        if ($('#fri_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()

            $('#id_fri_start_hr').val(mon_start_hr)
            $('#id_fri_start_ap').val(mon_start_ap)
            $('#id_fri_end_hr').val(mon_end_hr)
            $('#id_fri_end_ap').val(mon_end_ap)
        }
    });

    $('#sat_mon_copy').click(function () 
    {
        if ($('#sat_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()

            $('#id_sat_start_hr').val(mon_start_hr)
            $('#id_sat_start_ap').val(mon_start_ap)
            $('#id_sat_end_hr').val(mon_end_hr)
            $('#id_sat_end_ap').val(mon_end_ap)
        }
    });

    $('#sun_mon_copy').click(function () 
    {
        if ($('#sun_mon_copy').is(':checked') == true) 
        {
            var mon_start_hr    = $('#id_mon_start_hr').val()
            var mon_start_ap    = $('#id_mon_start_ap').val()
            var mon_end_hr      = $('#id_mon_end_hr').val()
            var mon_end_ap      = $('#id_mon_end_ap').val()
            
            $('#id_sun_start_hr').val(mon_start_hr)
            $('#id_sun_start_ap').val(mon_start_ap)
            $('#id_sun_end_hr').val(mon_end_hr)
            $('#id_sun_end_ap').val(mon_end_ap)
        }
    });



}); // AND OF JQUERY

function BlogFilterSubmit(slug)
{
    if(slug == 'All')
    {
        $('#id_category').val('')
    }
    else
    {
        $('#id_category').val(slug)
    }
    $('#blog_search_form').submit()
}

function changeLanguage(lang)
{
    $.ajax(
    {
        url: "/language/"+lang, 
        success: function(result)
        {
            location.reload()
        }
    });
}
