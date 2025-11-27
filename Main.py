import customtkinter as ctk

# -----------------------
# Linked List Logic
# -----------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_position(self, data, position):
        new_node = Node(data)
        if position <= 0 or not self.head:
            new_node.next = self.head
            self.head = new_node
            return True

        current = self.head
        index = 0

        while current.next and index < position - 1:
            current = current.next
            index += 1

        new_node.next = current.next
        current.next = new_node
        return True

    def delete_at_position(self, position):
        if not self.head:
            return False

        # Delete head
        if position == 0:
            self.head = self.head.next
            return True

        current = self.head
        index = 0
        prev = None

        while current and index < position:
            prev = current
            current = current.next
            index += 1

        if not current:
            return False

        prev.next = current.next
        return True

    def get_nodes(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(current.data)
            current = current.next
        return nodes


# -----------------------
# GUI Part (CustomTkinter)
# -----------------------
class LinkedListApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Linked List (Add/Delete by Position)")
        self.geometry("650x450")
        self.linked_list = LinkedList()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame for Inputs
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)

        # Value Entry
        ctk.CTkLabel(input_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
        self.value_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter node value")
        self.value_entry.grid(row=0, column=1, padx=5, pady=5)

        # Position Entry
        ctk.CTkLabel(input_frame, text="Position:").grid(row=0, column=2, padx=5, pady=5)
        self.position_entry = ctk.CTkEntry(input_frame, placeholder_text="Index (0-based)")
        self.position_entry.grid(row=0, column=3, padx=5, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(button_frame, text="Add Node", command=self.add_node)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = ctk.CTkButton(button_frame, text="Delete Node", command=self.delete_node)
        self.delete_button.grid(row=0, column=1, padx=10)

        # Canvas for Visual Linked List
        self.canvas = ctk.CTkCanvas(self, width=600, height=250, bg="#222")
        self.canvas.pack(pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack()

    # -----------------------
    # Functions
    # -----------------------
    def add_node(self):
        value = self.value_entry.get()
        pos = self.position_entry.get()

        if not value:
            self.status_label.configure(text="⚠ Please enter a node value.")
            return

        try:
            pos = int(pos)
        except ValueError:
            pos = 0  # default to head if invalid

        self.linked_list.insert_at_position(value, pos)
        self.value_entry.delete(0, 'end')
        self.position_entry.delete(0, 'end')
        self.update_display()
        self.status_label.configure(text=f"✅ Added node '{value}' at position {pos}")

    def delete_node(self):
        pos = self.position_entry.get()

        try:
            pos = int(pos)
        except ValueError:
            self.status_label.configure(text="⚠ Please enter a valid position.")
            return

        success = self.linked_list.delete_at_position(pos)
        if success:
            self.update_display()
            self.status_label.configure(text=f"🗑 Deleted node at position {pos}")
        else:
            self.status_label.configure(text=f"❌ Invalid position {pos} (no node found).")

        self.value_entry.delete(0, 'end')
        self.position_entry.delete(0, 'end')

    def update_display(self):
        self.canvas.delete("all")
        nodes = self.linked_list.get_nodes()
        x, y = 50, 130

        for i, data in enumerate(nodes):
            # Draw Node Box
            self.canvas.create_rectangle(x, y - 20, x + 60, y + 20, fill="#4a90e2", outline="white", width=2)
            self.canvas.create_text(x + 30, y, text=str(data), fill="white", font=("Arial", 12, "bold"))
            # Draw Index Label
            self.canvas.create_text(x + 30, y + 35, text=f"[{i}]", fill="#aaa", font=("Arial", 10))
            # Draw Arrow
            if i < len(nodes) - 1:
                self.canvas.create_line(x + 60, y, x + 90, y, arrow="last", fill="white", width=2)
                x += 90
            else:
                x += 60


# -----------------------
# Run the App
# -----------------------
if __name__ == "__main__":
    app = LinkedListApp()
    app.mainloop()
