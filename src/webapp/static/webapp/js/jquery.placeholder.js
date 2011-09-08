jQuery.fn.placeholder = function() 
{
	var counter=0;
	
	return this.each(function(){
		
		if ($(this).is("textarea"))
		{
			var placeholder = $(this).attr("placeholder");
			$(this).html(placeholder);
			
			$(this).css({color:'#999999',"font-style":"italic"});
			
			$(this).bind('focus', function(){
				if($(this).val()==placeholder)
				{
					$(this).val("");
					$(this).css({color:'inherit',"font-style":"normal"});
				}
			});
			
			$(this).bind('blur', function(){
                if($(this).val()==""){
					$(this).val(placeholder);
					$(this).css({color:'#999999',"font-style":"italic"});
				}
			});
		}
		else if ($(this).is("input")) {
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
						$(this).css({color:'inherit',"font-style":"normal"});
					}
				}
				)
				
				$(this).bind('blur', function()
				{
					if($(this).val()=="")
					{
						$(this).val(placeholder);
						$(this).css({color:'#999999',"font-style":"italic"});
					}
				}
				)
			}
		}
	});
}
