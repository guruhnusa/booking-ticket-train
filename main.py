from models.ticket_booking_app import TicketBookingApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()