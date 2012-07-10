import pyjd # this is dummy in pyjs

import random

from pyjamas.ui.HTML import HTML
from pyjamas import logging
from __pyjamas__ import JS
from __pyjamas__ import wnd

log = logging.getConsoleLogger()

def get_random_id():
    return "wav%s" % (random.randint(0, 10000))

class MySelect2TaggingComponent(HTML):

    def __init__(self, tags = None, width = 300, selected = None, myid = None):
        #log.info("tags='%s' width='%s' selected='%s'", tags, width, selected)
        if myid == None:
            myid = get_random_id()
        self.myid = myid
        self.tags = tags
        html  =  '<p><input type="hidden" id="%s" style="width:%dpx"/></p>' % (myid, width)
        html +=  '<div id="%s-show"></div>' % (myid)
        self.selected = selected
        log.info("html = '%s'", html)
        HTML.__init__(self, html)

    def change(self):
        log.info("event received!")

    def setup_js_show(self):
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

    def setup_pyjs_change(self):
        # This is supposed to bind the change event to the change pyjs function
        #   Not yet working
        wnd().change = self.change
        myjs = 'parent.jQuery("#%s").bind("change", change);' % (self.myid)
        #myjs = 'parent.jQuery("#%s").bind("change", self["change"]);' % (self.myid)
        #myjs = 'parent.jQuery("#%s").bind("change", this.change);' % (self.myid)
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)

    def final_setup(self):
        if self.tags:
            tags = ','.join(['"%s"' % (tag) for tag in self.tags])
        else:
            tags = ''
        myjs = 'parent.jQuery("#%s").select2({tags:[%s]});' % (self.myid, tags)
        # TODO: what about self.selected?
        log.info("Now calling JS: %s", myjs)
        JS(""" eval(@{{myjs}}) """)
        #self.setup_js_show()
        self.setup_pyjs_change()

    def get_val(self):
        myjs = 'parent.jQuery("#%s").select2("val");' % (self.myid)
        return JS(""" eval(@{{myjs}}) """)

    def update(self, tags, selected):
        pass

from pyjamas import Window
from pyjamas.ui.RootPanel import RootPanel

class MainWindow:

    def onModuleLoad(self):

        my_select2_tagging_component = MySelect2TaggingComponent()

        # Get rid of scrollbars, and clear out the window's built-in margin,
        # because we want to take advantage of the entire client area.
        Window.enableScrolling(False)
        Window.setMargin("0px")

        # Add the component to the DOM
        RootPanel().add(my_select2_tagging_component)

        # Now that it is in the DOM, select2 can perform the final setup
        my_select2_tagging_component.final_setup()

if __name__ == '__main__':
    pyjd.setup("./public/jQuerySelect2.html")
    w = MainWindow()
    w.onModuleLoad()
    pyjd.run()
