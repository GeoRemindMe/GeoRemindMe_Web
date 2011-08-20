jQuery.fn.placeholder = function() 
{
	$('textarea').each(function()
	{
		var placeholder = $(this).attr("placeholder");
		$(this).html(placeholder);
		
		$(this).css({color:'#999999',"font-style":"italic"});
		
		$(this).bind('focus', function()
		{
			if($(this).html()==placeholder)
			{
				$(this).html("");
				$(this).css({color:'#000'});
			}
		}
		)
		
		$(this).bind('blur', function()
		{
			if($(this).html()=="")
			{
				$(this).html(placeholder);
				$(this).css({color:'#999999'});
			}
		}
		)
	}
	);
	
	var counter=0;
	
	$('input').each(function()
	{
		var id = $(this).attr("id");
		var tabindex = $(this).attr("tabindex");
		var placeholder = $(this).attr("placeholder");
		
		if($(this).attr("type")=="password")
		{
			var thisdummy = 'dummy' + counter;
			
			$(this).hide();
			$(this).after('<input type="text" id="' + thisdummy + '"/>');
			$('#' + thisdummy).val(placeholder);
			if (tabindex) $('#' + thisdummy).attr("tabIndex",tabindex);
			$('#' + thisdummy).css({color:'#999999',"font-style":"italic"});
			
			counter++;
			
			$('#' + thisdummy).bind('focus', function()
			{
				$("#" + id).show().val("");
				$("#" + id).show().focus();
				$(this).hide();
			}
			)
			
			$(this).bind('blur', function()
			{
				if($(this).val()=="")
				{
					$(this).hide();
					$("#" + thisdummy).show();
				};
			}
			)
		}
		
		if($(this).attr("type")=="text")
		{
			$(this).val(placeholder);
			$(this).css({color:'#999999',"font-style":"italic"});
			
			$(this).bind('focus', function()
			{
				if($(this).val()==placeholder)
				{
					$(this).val("");
					$(this).css({color:'#000'});
				}
			}
			)
			
			$(this).bind('blur', function()
			{
				if($(this).val()=="")
				{
					$(this).val(placeholder);
					$(this).css({color:'#999999'});
				}
			}
			)
		}
	}
	);
};
