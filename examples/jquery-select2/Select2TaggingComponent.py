from pyjamas.ui.HTML import HTML
from pyjamas import logging
from __pyjamas__ import JS
from __pyjamas__ import wnd

log = logging.getConsoleLogger()

class Select2TaggingComponent(HTML):

    def __init__(self, tags = None, width = 300, selected = None, myid = 'select2example'):
        #log.info("tags='%s' width='%s' selected='%s'", tags, width, selected)
        self.myid = myid
        self.tags = tags
        # This markup is used by select2 to configure the component
        html  =  '<p><input type="hidden" id="%s" style="width:%dpx"/></p>' % (myid, width)
        html +=  '<div id="%s-show"></div>' % (myid)
        self.selected = selected
        log.info("html = '%s'", html)
        HTML.__init__(self, html)

    def get_val(self):
        # This uses select2 to get the value of the element
        myjs = 'parent.jQuery("#%s").select2("val");' % (self.myid)
        return JS(""" eval(@{{myjs}}) """)

    def change(self):
        # This will be fired whenever the select2 component changes
        pass

    def update(self, values):
        values_js = []
        for value in values:
            values_js.append('{id:"%s", text:"%s"}' % (value['id'], value['text']))
        values_js = ','.join(values_js)
        myjs = 'parent.jQuery("#%s").select2("val", [%s]);' % (self.myid, values_js)
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)

    def bind_js_show(self):
        # This is a pure javascript function, which can be triggered by binding with jQuery
        #   the "change" event to it
        show = '''
         function show() {
                var e=parent.jQuery("<div style='background-color:yellow;'>change fired</div>");
                parent.jQuery("#%s-show").append(e);
                e.animate({opacity:0}, 1000, 'linear', function() { e.remove(); });
            };''' % (self.myid)
        myjs = '%s parent.jQuery("#%s").bind("change", show);' % (show, self.myid)
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)

    def bind_pyjs_change(self):
        # Here bind the change event to the self.change pyjs method
        # First bind the wnd().change JS function to the self.change method
        # TODO: this will bind ALL the wnd().change function to the last Select2TaggingComponent
        #  component created, effectively preventing having more than one
        wnd().change = self.change
        # Now bind the change event to the wnd().change JS function, which is actually the pyjs self.change method
        myjs = 'parent.jQuery("#%s").bind("change", function() { parent.change() });' % (self.myid)
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)

    def final_setup(self):
        # Since select2 acts on the DOM, this can only be called once the component has been added to the DOM.
        if self.tags:
            tags = ','.join(['"%s"' % (tag) for tag in self.tags])
        else:
            tags = ''
        myjs = 'parent.jQuery("#%s").select2({tags:[%s]});' % (self.myid, tags)
        # TODO: what about self.selected?
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)
        self.bind_js_show()       # Bind a jQuery function
        self.bind_pyjs_change()   # Bind a pyjs method

