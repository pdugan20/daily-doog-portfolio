jQuery('.mobile_app_menu_main_wrapper .header-back-to-blog-link').on('click', function(){
  maToggleMenu();
});
	
jQuery('.mobile-menu-open-wrapper').click(function(){
  maToggleMenu();
});
	
jQuery('.mobile-menu-settings-wrapper').click(function(){
  if(jQuery('body').hasClass('mobile-app-settings-panel')){
    jQuery('body').removeClass('mobile-app-settings-panel');
	jQuery('.mobile_app_settings_wrapper').removeClass('mobile_app_settings_wrapper-visible');
  }else{
    jQuery('body').addClass('mobile-app-settings-panel');
    jQuery('.mobile_app_settings_wrapper').addClass('mobile_app_settings_wrapper-visible');
  }
});

function maToggleMenu(){
	if(jQuery('#mobile_app_menu').hasClass('mobile-menu-open-visible')){
		// Removes background transparency fade-in
		/* $('.mobile_app_menu_main_wrapper-visible').css({backgroundColor: 'transparent'}); */
		
		jQuery('.mobile-menu-open-wrapper').removeClass('mobile-menu-open-wrapper-active');
		jQuery('#mobile_app_menu').removeClass('mobile-menu-open-visible');
		
		/* Fixed */
		jQuery('body').removeClass('mobile-menu-open-fixed');
		jQuery('.mobile_app_menu_main_wrapper').removeClass('mobile_app_menu_main_wrapper-visible');
	}else{
		/* jQuery('meta[name*="viewport"]').attr('content', 'user-scalable=yes, width=635'); */
		jQuery('.mobile-menu-open-wrapper').addClass('mobile-menu-open-wrapper-active');
		jQuery('#mobile_app_menu').addClass('mobile-menu-open-visible');
		
		/* Fixed */
		jQuery('body').addClass('mobile-menu-open-fixed');
		jQuery('.mobile_app_menu_main_wrapper').addClass('mobile_app_menu_main_wrapper-visible');
		
		// Animates background transparency fade-in
		/* $('.mobile_app_menu_main_wrapper-visible').animate({backgroundColor: 'rgba(228, 228, 228, 0.9)'}, 300); */
	}
}