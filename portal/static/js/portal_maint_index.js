$(document).ready(function(){


	$(".datatable_display").each(function(index){
		var strJsonURL = $(this).attr('json_url');
		$(this).dataTable( {
		        "bJQueryUI": true,
		        "bProcessing": true,
		        "sAjaxSource": strJsonURL,
		    });
	});  


	$( "#digConfirm" ).dialog({
		 
		autoOpen: false
		 
	}); 
	$( "#digblank" ).dialog({
		 
		autoOpen: false
		 
	}); 
	
	$( "#digReturn" ).dialog({
		 
		autoOpen: false
		 
	}); 


});
function MessageWarning(varLabel)
{
	var objName = "#digReturn";
	$(objName).find(".error-content").html(varLabel );
	$(objName ).dialog({autoOpen: true});
		
} 
function MessageNotBlank(varLabel)
{
	var objName = "#digblank";
	$(objName).find(".error-content").html(varLabel + " can not be blank.");
	$(objName ).dialog({autoOpen: true});
		
}
function deleteConfirm(objThis)
	{	
		var rowMessage = $(objThis).attr("delete-message");
		

		console.log('ok here');
		$("#digConfirm").find(".error-content").html("Are you sure you want to remove " +  rowMessage);
		$( "#digConfirm" ).dialog({
			resizable: false,
			autoOpen: true, 
			height: "auto",
			modal:true,
			width: 400, 
			buttons: {
				"Delete": function() {
					var strTable = $(objThis).closest("table").attr('id'); 
					var strID = $(objThis).attr("delete-id"); 
					var strJsonURL =$("#" + strTable).attr('json_url');
					var rowURL = $("#" + strTable).attr("delete-url")  ;
					 $.ajax({
						type: "POST",
						url: rowURL,
						dataType: "json",
						data: { actionType : "DELETE" ,ID :strID },
						success: function(payload) {
							var test = $("#" + strTable).dataTable();
							test.fnDestroy();
							$("#" + strTable).dataTable( {
								"bJQueryUI": true,
								"bProcessing": true,
								"sAjaxSource": strJsonURL,
							    });
						},
						error: function(XMLHttpRequest, textStatus, errorThrown) {
						//alert(XMLHttpRequest.responseText);
						return this;
						}
					});  
					
					//$("#" + strTable).fnDestroy();
					
					$( this ).dialog( "close" );
				},
				Cancel: function() {
				$( this ).dialog( "close" );
				}
			}
		}); 
	}
