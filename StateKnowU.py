class StateKnowU(State):
    def handle_command(self, command):
        if "=" in command:
            key, value = command.split("=")
            if key.lower() == "i":
                self.server.value_i = parse_value(value)
                self.server.state = StateKnowUandI(self.server)
                return "OK"
            elif key.lower() == "r":
                self.server.value_r = parse_value(value)
                self.server.state = StateKnowUandR(self.server)
                return "OK"
        elif command.lower() == "u=?":
            return f"U={self.server.value_u}V"
        return "Invalid input or not enough data to calculate."
