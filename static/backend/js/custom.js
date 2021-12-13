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
            url: "/backend/cities/"+this.value, 
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
            url: "/backend/subcategories/"+this.value, 
            success: function(result)
            {
                $('#id_subcategory').html(result)
            }
        });

    });

    $('#id_plan').on('change', function() 
    {
        if(this.value != '')
        {
            $.ajax(
            {
                url: "/backend/plan/detail/"+this.value, 
                success: function(result)
                {
                    $('#id_payment_amount').val(result.amount)
                    $('#id_startdate').val(result.startdate)
                    $('#id_enddate').val(result.enddate)
                }
            });
        }
    });

}); // AND OF JQUERY

function ActionForm(val)
{
    if($('.chk:checked').length == 0)
    {
        alert('Records must be selected in order to perform actions on them.')
    }
    else
    {
        $("#action_on").val(val)
        $("#action_form").submit()
    }
}

function SendRequest(val)
{
    if($('.chk:checked').length == 0)
    {
        alert('Records must be selected in order to perform actions on them.')
    }
    else
    {
        $("#action_form").submit()
    }
}