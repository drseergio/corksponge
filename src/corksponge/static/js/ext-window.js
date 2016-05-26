Ext.namespace('Ext.ux');

Ext.ux.CorkWindow = Ext.extend(Ext.Window, {
    setActive : function(active){
        if(active){
            this.fireEvent('activate', this);
        }else{
            this.fireEvent('deactivate', this);
        }
    },
});

Ext.reg('corkwindow', Ext.ux.CorkWindow);
