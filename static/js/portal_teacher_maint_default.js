 	function removeCountry(strObj)
	{
		
	}

	function isNumber(evt) {
	    evt = (evt) ? evt : window.event;
	    var charCode = (evt.which) ? evt.which : evt.keyCode;
	    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
		return false;
	    }
	    return true;
	}
	function replaceAll(str, find, replace) {
	    return str.replace(new RegExp(find, 'g'), replace);
	}
	$( document ).ready(function() {
		$(".EditReadOnly").each(function(index){
			$(this).removeAttr("readonly");
			if( !($("#txtid").val()=="" || $("#txtid").val()=="0"))
			{
				console.log('txtid: ' ,$("#txtid").val());
				$(this).attr("readonly","true");
			}
			
		});
		  
		$("#btnSave").click(function(){
			var strID = $("#txtid").val();
			if (strID == "")
				strID = "0";
			var lst_data_post = [{"Field" : "ID", "Value" :   strID    }]
			var isError = false;
			$(".EditField").each(function(index){
				var strField = $(this).attr('field');
				var strMandatory = $(this).attr('mandatory');
				var strLabelDesc = $(this).attr('label-desc');
				var strIsNumeric = $(this).attr('isNumeric');
				var isTinyMCE = $(this).attr('TinyMCE');
				var strValue = $(this).val(); //.replace(/"/g, '\\"');
				if($(this).is(":checkbox")) {
					console.log($(this), " is checkbox");
				}
				if($(this).is("textarea"))
				{
                                	if(isTinyMCE=="YES")
					{
						console.log('is tinymce:',$(this).attr('id'));
						//var content =  tinymce.getContent($(this).attr('id'));
						var content =  tinyMCE.get($(this).attr('id')).getContent()
						strValue = replaceAll(content,'"','\'');
						//strValue = strValue.replace('"','\'');
						strValue = escape(strValue);
						//console.log('content:',content);
					}
					else
					{
						strValue = replaceAll(strValue,'"','\'');
						//strValue = strValue.replace('"','\'');
						strValue = escape(strValue);
					}
					
					
				}
				var lst_array ={"Field" :    strField , "Value" :    strValue    };
				
				//lst_data_post.push(lst_array);
				console.log("Field: " , strField, "Value: " ,strValue);
				lst_data_post.push(lst_array);
				if (strMandatory == "TRUE" && strValue == "")
				{
					isError = true;
					console.log(this , strLabelDesc);
					MessageNotBlank(strLabelDesc);
					return false;
				}
				if (strIsNumeric=="TRUE")
				{
					if(!isNumber(strValue))
					{
						isError = true;
						MessageWarning(strLabelDesc + " must be numeric.");
						return false;
					}
				}
				 
			}); 
			console.log('lst_data_post: ' , lst_data_post);
			  console.log("isError " , isError);
			if(isError) return;
				//data:  JSON.stringify(lst_data_post),
			$.ajax({
				type: "POST",
				url: strURL_action_default,
				dataType: "json",
				data:    JSON.stringify(lst_data_post)  ,
				success: function(payload) {
						$('#txtid').val(payload["ID"])
						if(payload["return"]!="ok")
						{
							console.log('return', payload);
							var objName = "#digReturn";
							$(objName).find(".error-content").html(payload["return"] );
							$(objName ).dialog({autoOpen: true});
							return;
						}
						else{
							if (typeof EndSaveTransaction == 'function') {
								EndSaveTransaction();
							    }
							console.log('txtid', $('#txtid').val());
							$( "#dialog-message" ).dialog({
								modal: true,
								buttons: {
									Ok: function() {
									$( this ).dialog( "close" );
									}
								}
							}); 
						}
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					$( "#dialog-error" ).dialog({
						modal: true,
						buttons: {
							Ok: function() {
							$( this ).dialog( "close" );
							}
						}
					}); 
					return this;
				}
			});
		});
	});
