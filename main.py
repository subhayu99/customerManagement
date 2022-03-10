from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.accordion import Accordion, AccordionItem
from invoicepdf import invoice

Builder.load_file("main.kv")

class MyAccordionItem(AccordionItem):
    pass

class MyAccordion(Accordion):
    def __init__(self, **kwargs):
        super(MyAccordion, self).__init__(**kwargs)

        for i in range(1, 5):
            accordionitem = MyAccordionItem(title=f"Item {i}")
            self.add_widget(accordionitem)

class MyGridLayout(Widget):
    def press(self):
        invoice_num = self.ids.invoice_num.text
        customer = self.ids.customer.text
        paid = self.ids.paid.text
        booking_date = self.ids.booking_date.text
        check_in = self.ids.check_in.text
        check_out = self.ids.check_out.text
        heads = self.ids.heads.text
        
        item_desc = self.ids.item_desc.text.split("\n")
        addons = self.ids.addons.text.split("\n")
        price = self.ids.price.text.split("\n")
        qty = self.ids.qty.text.split("\n")

        items = []
        items_len = 0
        for (i, j, k, l) in zip(item_desc, addons, price, qty):
            item = [i, j, k, l]
            items_len += len(''.join(item))
            if items_len != 0:
                items.append(item)


        every_len = len(f"{invoice_num}{customer}{paid}{booking_date}{check_in}{check_out}{heads}")+items_len
        print(every_len)
        if every_len != 0:
            invoice(invoice_num, customer, paid, booking_date, check_in, check_out, heads, items)
            self.ids.message_label.text = "Details have been Submitted"
        else:
            self.ids.message_label.text = "Some values are missing!!"

class MyApp(App):

    def build(self):
        # change background color
        Window.clearcolor = (1, 1, 1, 1)
        
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()