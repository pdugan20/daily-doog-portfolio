// center images inside elements
function centerIsotypeImages(){
	jQuery('.element').each(function(){
		var $this = jQuery(this);

		// Center images
		if($this.find('img').get(0) === undefined){ return; }
		var cont_ratio = $this.width() / $this.height();
		var img_ratio = $this.find('img').get(0).width / $this.find('img').get(0).height;

		if(cont_ratio <= img_ratio){
			$this.find('img').css({ 'width' : '220px', 'height' : '320px', 'top' : 0 }).css({ 'left' : ~(($this.find('img').width()-$this.width())/2)+1 });
			$this.find('img').addClass('project-img-visible');
		}else{
			$this.find('img').css({ 'width' : '220px', 'height' : '320px', 'left' : 0 }).css({ 'top' : ~(($this.find('img').height()-$this.height())/2)+1 });
			$this.find('img').addClass('project-img-visible');
		}
	});
}
jQuery(window).load(function(){
	centerIsotypeImages();
});
jQuery(document).ready(function(){
    
    var $container = jQuery('#container');
    var $containerSmall = jQuery('#content-small');

      // add randomish size classes
      $container.find('.element').each(function(){
        var $this = jQuery(this),
            number = parseInt( $this.find('.number').text(), 10 );
        if ( number % 7 % 2 === 1 ) {
          $this.addClass('width2');
        }
        if ( number % 3 === 0 ) {
          $this.addClass('height2');
        }        
		if ( number % 7 === 0 ) { //Rare because it picks random number from 1 to 11 and only 7 matches criteria
          $this.addClass('width3');
          $this.addClass('height2');
        }
      });
	
	// Center images inside thumbnails on window resize end
	var TO = false;
	jQuery(window).bind("resize.centerisotypeimages", function(){
		if(TO !== false){
			clearTimeout(TO);
		}
		TO = setTimeout(centerIsotypeImages, 200);
	});

	// Snippet below is present because individual images load earlier than global window load happens
	jQuery(".project-img").one("load",function(){
		var $this = jQuery(this);
		var cont_ratio = $this.parent().width() / $this.parent().height();
		var img_ratio = $this.get(0).width / $this.get(0).height;
		if(cont_ratio <= img_ratio){
			$this.css({ 'width' : 'auto', 'height' : '100%', 'top' : 0 }).css({ 'left' : ~(($this.width()-$this.parent().width())/2)+1 });
			$this.addClass('project-img-visible');
		}else{
			$this.css({ 'width' : '100%', 'height' : 'auto', 'left' : 0 }).css({ 'top' : ~(($this.height()-$this.parent().height())/2)+1 });
			$this.addClass('project-img-visible');
		}
	});
	
	    
    $container.isotope({
      itemSelector : '.element',
      masonry : {
        //columnWidth : 120
        columnWidth : 5,
		gutterWidth: 5,
      },
      masonryHorizontal : {
        rowHeight: 120
      },
      cellsByRow : {
        columnWidth : 240,
        rowHeight : 240
      },
      cellsByColumn : {
        columnWidth : 240,
        rowHeight : 240
      },
      getSortData : {
        symbol : function( $elem ) {
          return $elem.attr('data-symbol');
        },
        category : function( $elem ) {
          return $elem.attr('data-category');
        },
        number : function( $elem ) {
          return parseInt( $elem.find('.number').text(), 10 );
        },
        weight : function( $elem ) {
          return parseFloat( $elem.find('.weight').text().replace( /[\(\)]/g, '') );
        },
        name : function ( $elem ) {
          return $elem.find('.name').text();
        }
      }
    });
    
    
	var $optionSets = jQuery('#options .option-set'),
	$optionLinks = $optionSets.find('a');

	$optionLinks.click(function(){
		var $this = jQuery(this);
		// don't proceed if already selected
		if ( $this.hasClass('selected') ) {
			return false;
		}
		var $optionSet = $this.parents('.option-set');
		$optionSet.find('.selected').removeClass('selected');
		$this.addClass('selected');

		// make option object dynamically, i.e. { filter: '.my-filter-class' }
		var options = {},
			key = $optionSet.attr('data-option-key'),
			value = $this.attr('data-option-value');
		// parse 'false' as false boolean
		value = value === 'false' ? false : value;
		options[ key ] = value;
		if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ){
			// changes in layout modes need extra logic
			changeLayoutMode( $this, options );
		}else{
			// otherwise, apply new options
			$container.isotope( options );
		}

		return false;
	});

	// change layout
	var isHorizontal = false;
	function changeLayoutMode( $link, options ) {
		var wasHorizontal = isHorizontal;
		isHorizontal = $link.hasClass('horizontal');

		if ( wasHorizontal !== isHorizontal ) {
			// orientation change
			// need to do some clean up for transitions and sizes
			var style = isHorizontal ? 
			{ height: '80%', width: $container.width() } : 
			{ width: 'auto' };
			// stop any animation on container height / width
			$container.filter(':animated').stop();
			// disable transition, apply revised style
			$container.addClass('no-transition').css( style );
			setTimeout(function(){
				$container.removeClass('no-transition').isotope( options );
			}, 100 )
		} else {
			$container.isotope( options );
		}
	}
		
	
	// close bringPortfolio()
	//jQuery('#compact_navigation_container').delegate('.header-back-to-blog-link', 'click', function(){
	jQuery('.header-back-to-blog-link').on('click', function(){
		// If button is supposed to redirect to some external URL
		if(jQuery(this).hasClass('back-link-external')){ return; }
		// Usual action of button
		jQuery('.portfolio_box').removeClass('portfolio_box-visible');
		jQuery('body').removeClass('daisho-portfolio-viewing-project');
		jQuery('#compact_navigation_container').removeClass('compact_navigation_container-visible');
		jQuery('.project-coverslide').removeClass('project-coverslide-visible');
		jQuery('.project-navigation').removeClass('project-navigation-visible');
		jQuery('.portfolio-arrowright').removeClass('portfolio-arrowright-visible');
		jQuery('.portfolio-arrowleft').removeClass('portfolio-arrowleft-visible');
		jQuery('.project-slides').empty();
		jQuery('title').text(homepage_title);
		var document_title = "Daisho WordPress Theme";
		var portfoliohistorywpurl = "daisho";
		window.history.pushState({}, document_title, ((portfoliohistorywpurl)?("/"+portfoliohistorywpurl+""):"/"));
	});

	// Close project on background click
	/* jQuery(document).on('click', '.project-coverslide', function(){
		closePortfolioItem();
	}); */
 
	// change size of clicked element
	$container.delegate( '.element', 'click', function(){
		if(jQuery(this).find('.thumbnail-link').length != 0){ return; }
		var current_id = jQuery(this).find('.id').text();
		bringPortfolio(current_id);
		portfolio_closenum = 0;
		portfolio_closedir = false;
	});
	
	// Prevent thumbnail links from working unless they are external links. They are for search engines only. In no-js mode it's going to enable links.
	$container.on('click', '.thumbnail-project-link', function(e){
		e.preventDefault();
	});
	$containerSmall.on('click', '.thumbnail-project-link', function(e){
		e.preventDefault();
	});
	
	// change size of clicked element (small)
	$containerSmall.on('click', '.element', function(){
		if(jQuery(this).find('.thumbnail-link').length != 0){ return; }
		var current_id = jQuery(this).find('.id').text();
		bringPortfolio(current_id);
	});

	// toggle variable sizes of all elements
	jQuery('#toggle-sizes').find('a').click(function(){
		if(jQuery(this).hasClass('toggle-selected')){ return false; }
		jQuery('#toggle-sizes').find('a').removeClass('toggle-selected');
		jQuery(this).addClass('toggle-selected');
		if(!jQuery('#toggle-sizes a:first-child').hasClass('toggle-selected')){
			$container.find('.element').addClass('element-small'); 
		}else{ 
			$container.find('.element').removeClass('element-small'); 
		}

		$container
			.toggleClass('variable-sizes')
			.isotope('reLayout');
		centerIsotypeImages();
		return false;
	});

	var $sortBy = jQuery('#sort-by');
	jQuery('#shuffle a').click(function(){
		$container.isotope('shuffle');
		$sortBy.find('.selected').removeClass('selected');
		$sortBy.find('[data-option-value="random"]').addClass('selected');
		return false;
	});
});