#!/usr/bin/python3

from kivy.app import App
from kivymd.app import MDApp
from datetime import datetime
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from invoicepdf import invoice
from kivymd.uix.picker import MDDatePicker, MDTimePicker

Builder.load_file("main.kv")

class MyGridLayout(Widget):
    # Click OK
    def on_booking_date_save(self, instance, value, date_range):
        # print(instance, value, date_range)
        self.ids.booking_date.text = str(value.strftime("%d/%m/%Y"))

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_booking_date_save)
        date_dialog.open()


    def set_check_in_time(self, instance, time):
        self.ids.check_in.text = str(time.strftime("%I:%M %p"))

    def show_check_in_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.strptime("12:00:00", '%H:%M:%S').time())
        time_dialog.bind(time=self.set_check_in_time)
        time_dialog.open()


    def set_check_out_time(self, instance, time):
        self.ids.check_out.text = str(time.strftime("%I:%M %p"))

    def show_check_out_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.set_time(datetime.strptime("10:00:00", '%H:%M:%S').time())
        time_dialog.bind(time=self.set_check_out_time)
        time_dialog.open()

    def selected_item(self, value):
        self.ids.item_desc.text += f"{value}\n"

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
        item_missing = False
        if len(item_desc) == len(addons) == len(price) == len(qty):
            if not "" in item_desc and not "" in addons and not "" in price and not "" in qty:
                for (i, j, k, l) in zip(item_desc, addons, price, qty):
                    item = [i, j, k, l]
                    items_len += len(''.join(item))
                    if items_len != 0:
                        items.append(item)
            else:
                item_missing = True
        else:
            item_missing = True


        every_len = len(f"{invoice_num}{customer}{paid}{booking_date}{check_in}{check_out}{heads}")+items_len
        print(f"""
        invoice_num: {invoice_num}
        customer: {customer}
        paid: {paid}
        booking_date: {booking_date}
        check_in: {check_in}
        check_out: {check_out}
        heads: {heads}
        items: {items}
        items_len: {items_len}
        """)
        if every_len:
            if paid:
                if not item_missing:
                    print(items)
                    invoice(invoice_num, customer, paid, booking_date, check_in, check_out, heads, items)
                    self.ids.message_label.text = "Details have been Submitted"
                else:
                    self.ids.message_label.text = "Some items do not have values!"
            else:
                self.ids.message_label.text = "Amount Paid is missing!"
        else:
            self.ids.message_label.text = "Some values are missing!"

class SandCastles(MDApp):

    def build(self):
        # change background color
        # Window.clearcolor = (1, 1, 1, 1)
        self.theme_cls.theme_style = "Light"

        return MyGridLayout()


if __name__ == '__main__':
    SandCastles().run()