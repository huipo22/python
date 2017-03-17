$(document).ready(function(){
	$('img').parent().css({'display':'flex','justify-content':'center','align-items':'center','height':'auto'})
  	var IsWife=parseInt($('input[type="hidden"]').val());
	if(IsWife==1){
		getBigImg();
	}else if(IsWife==0){
		getSmallImg();
	}else{
		getSmallImg();
	}
	$('img.smallimg').click(function(){
		var index=$('img.smallimg').index(this);
		var  images  =  all_images.images;
		$(this).attr({'src':images[index],'class':'bigimg'})
		$(this).click ( function(){
		var imgid = $(this).parent().attr('id');
		var img = imgid.substr(4); 
					window.location.href="#images"+img;
						console.log(img);
		}); 
	})
});

function getBigImg(){
	var images = all_images.images;
	var content_str = $(".content").html()
		for(var i = 0;i < images.length ; i++) {
				console.log(images[i]);
				$("#IMG_" + i).html("<img class='bigimg' src='" + images[i] + "' />")
				$("#IMG_"+ i).click ( function(){
				 var img = this.id.substr(4); 
					window.location.href="images"+img;
			    }); 
			}
		}

function getSmallImg(){
	var smallimg = all_images.not_wifi;
	var content_str = $(".content").html();
			for(var i = 0 ; i < smallimg.length ; i++) {
				console.log(smallimg[i]);
				$("#IMG_" + i).html("<img class='smallimg' src='" + smallimg[i] + "' />")
				$("#IMG_"+ i).css('background','none')
			}
		}
