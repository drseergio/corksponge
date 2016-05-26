/*
*	@class			: Ext.ux.DDScrollingPanel
*	@extends		: Ext.Panel
*	@description	: Example implementation of using Ext.dd.DragZone (DD feature) to scroll the body of Ext.Panel
*	@author			: Totti Anh Nguyen
*	@version		: 0.1

In a panel where the content area is huge but the Panel is small,
users usually use MouseWheel to scroll vertically Up and Down.
However, this DD feature allows users to scroll both vertically and horizontally by dragging and dropping
the body of Ext.Panel.

In this entry, I'll walk you guys through a simple implementation of scrolling Ext.Panel
Vertically and Horizontally by Dragging and Dropping using Ext.dd.DragZone.

Examples of sites having this feature:
1. maps.google.com
2. gothere.sg

*/
Ext.ns('Ext.ux');
Ext.ux.DDScrollingPanel = Ext.extend(Ext.Panel, {
	/*
	*	@config	
	* 	dragOutOfBound	Allows users to drag the content of Panel when mouse is outside the bound of panel. Default to true.
	*/
	dragOutOfBound: true,
	
	// Extension specific CSS config
	/*
	*	@config		bodyCssClass	CSS class of the opened_hand.cur cursor. 
									To be appended by other custom classes if users use this property for other purposes.
	*/
	bodyCssClass: 'x-panel-wrap-dd-area',
	
	/*
	*	@config		handCursorCssClass	CSS class of the closed_hand.cur cursor.
	*/
	handCursorCssClass: 'x-panel-wrap-dd-area-scrolling',
		
	// Set the cursor
	// Could be put in a subclass of Ext.Panel
	setDragCursor: function(dragging) {
		var c = this.body,
			cls = this.handCursorCssClass;
		
		if (dragging) {
			if (!c.hasClass(cls)) {
				c.addClass(cls);
			}
		} else {
			c.removeClass(cls);
		}
	},
	
	initEvents: function() {		
		var p = this;
		
		p.ddScrollZone = new Ext.dd.DragZone(p.body, 		// Body element of the panel is our DragZone
		{
			dragOutOfBound: Ext.isDefined(p.dragOutOfBound) ? p.dragOutOfBound : true,
			
			// On receipt of a mousedown event, see if it is within a DataView node.
			// Return a drag data object if so.
			getDragData: function(e) {
				this.ddscrolling = true;		// User is DD scrolling								
				
				if (!this.ddel) {
					this.ddel = document.createElement('div');
					this.ddel.innerHTML = "Testing";
				}
				
				return this.dragData = {					
					ddel: this.ddel
				};
			},
			
			// On every drag event, we scroll the body of Ext.Panel			
			onDrag: function(e) {
				
				if (this.ddscrolling) {
					// Hide the proxy as we don't need it
					this.hideProxy();										
					
					// Calculate the scrolling position
					var	pb = p.body, 						
						b = pb ? pb.dom : false;
					if (b) {
					
						// Initialize Drag and Drop coordinates
						if (!Ext.isDefined(this.lastDDX)) {
							this.lastDDX = 0;
							this.lastDDY = 0;
						}
						
						// Get position of the mouse
						var r = pb.getRegion(),
							xy = e.getXY(),
							x = xy[0], 
							y = xy[1];
						
						// Check to prevent drag and drop when mouse is out of the bound of the panel
						if (this.dragOutOfBound || ((x < r.right) && (x > r.left) && (y < r.bottom) && (y > r.top))) {
							
							var
							sx = x - this.lastDDX,
							sy = y - this.lastDDY,
							
							sl = parseInt(b.scrollLeft, 10) - parseInt(sx, 10),
							st = parseInt(b.scrollTop, 10) - parseInt(sy, 10);
							
							// Check to prevent flickering
							if (sl >= 0 && st >= 0) {
								b.scrollLeft = sl;
								b.scrollTop = st;
							}
							
							// Save the last Drag and Drop coordinates
							this.lastDDX = x;
							this.lastDDY = y;
						}												
					}
				}
				
			},
			
			onStartDrag : function( target, e, id ){
				// Change the cursor to 'closed_hand'
				p.setDragCursor(true);
			},
			
			onEndDrag : function(data, e){
				// Change the cursor back to 'open_hand'
				p.setDragCursor(false);
				
				// Reset the last Drag and Drop coordinates
				this.lastDDX = 0;
				this.lastDDY = 0;
			}
			
		});
		
		Ext.ux.DDScrollingPanel.superclass.initEvents.call(this);
	},

	beforeDestroy : function(){
        Ext.ux.DDScrollingPanel.superclass.beforeDestroy.call(this);
		
		if(this.rendered){
            Ext.destroy(this.ddScrollZone);
		}
	}
});

Ext.reg('ddscrollpanel', Ext.ux.DDScrollingPanel);
