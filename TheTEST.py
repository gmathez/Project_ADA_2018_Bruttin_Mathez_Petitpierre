from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout

string_to_build_recycleview = '''
<rowTest@BoxLayout>:
    canvas:
        Rectangle:
            size: self.size
            pos: self.pos
    a_number: '5'
    TextInput:
        padding: (8, 1, 2, 1)
        halign: 'middle'
        size_hint_x: .8
        multiline: 'False'
        input_filter: 'int'
        text: root.a_number
        on_text: root.a_number = self.text
        on_text: if self.focus: root.parent.target_id.text = 'temp value: %s' % self.text

<RecycleViewTEST@RecycleView>:
    id: myListToTest
    scroll_type: ['bars', 'content']
    scroll_wheel_distance: dp(114)
    bar_width: dp(10)
    viewclass: 'rowTest'
    target_id: None

    RecycleBoxLayout:
        default_size: None, dp(20)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(2)
        target_id: root.target_id
 '''


class RecycleViewTEST(RecycleView):
    def __init__(self, **kwargs):
        super(RecycleViewTEST, self).__init__(**kwargs)
        Builder.load_string(string_to_build_recycleview)
        self.populate_1()

    def populate_1(self):
        self.data = [{'a_number': '1'}, {'a_number': '2'}, {'a_number': '3'}, {'a_number': '0'}, {'a_number': '0'}]
        print(self.data)

    def populate_2(self):
        self.data = [{'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}]
        print(self.data)

    def populate_3(self):
        self.data = [{'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}, {'a_number': '0'}]
        print(self.data)

string_to_build_the_form = '''
<TheForm>:
    Button:
        size_hint: (None, None)
        size: (180, 27)
        pos_hint: {'x': .05, 'y': .9}
        id: btt1
        text: 'Populate with 1'
        on_release: myListToTest.populate_1()
    Button:
        size_hint: (None, None)
        size: (180, 27)
        pos_hint: {'x': .35, 'y': .9}
        id: btt2
        text: 'Populate with 2'
        on_release: myListToTest.populate_2()
    Button:
        size_hint: (None, None)
        size: (180, 27)
        pos_hint: {'x': .65, 'y': .9}
        id: btt3
        text: 'Populate with 3'
        on_release: myListToTest.populate_3()
    BoxLayout:
        size_hint: .9,.25
        pos_hint: {'x':.05, 'y':.6}
        RecycleViewTEST:
            id: myListToTest
            target_id: target

    Label:
        id: target
'''


class TheForm(FloatLayout):
    def __init__(self, **kwargs):
        super(TheForm, self).__init__(**kwargs)
    Builder.load_string(string_to_build_the_form)


class TheTEST(App):
    def build(self):
        sm = TheForm()
        return sm

if __name__ == '__main__':
    TheTEST().run()