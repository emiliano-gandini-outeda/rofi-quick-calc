#!/usr/bin/env python3
import subprocess
import math
import sys

history = []

def calculate(expr):
    try:
        expr = expr.strip()
        if not expr:
            return None
            
        # Allow math functions and basic operations
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed.update({'abs': abs, 'round': round, 'min': min, 'max': max, 'pow': pow})
        
        result = eval(expr, {"__builtins__": {}}, allowed)
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.8g}"
        return str(result)
    except:
        return None

def run_calculator():
    current_input = ""
    
    while True:

        # Build display text
        display_items = []
    
        # Always show full history (without filtering)
        display_items.extend(reversed(history[-10:]))  # Show last 10 items
        
        display_text = "\n".join(display_items)
        
        try:
            # Run rofi with filtering disabled
            cmd = [
                "rofi",
                "-dmenu",
                "-p", "Calc:",
                "-theme", "Adapta-Nokto",
                "-format", "s",
                "-no-fixed-num-lines",
                "-filtering", "false",  
                "-lines", "12"
            ]
            
            result = subprocess.run(
                cmd,
                input=display_text,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            # Close if user presses Escape
            if result.returncode == 1:
                sys.exit(0)
            elif result.returncode != 0:
                print(f"Error: Rofi exited with code {result.returncode}")
                sys.exit(1)
                
            user_input = result.stdout.strip()
            
            if not user_input:
                continue
                
            # Check if user selected a history item (contains " = " and is in history)
            if " = " in user_input and any(user_input == entry for entry in history): # This isn't working
                # Extract the expression from history and set as current input
                current_input = user_input.split(" = ")[0]
                continue
                
            # Check if user selected the separator
            if user_input.startswith("─"):
                continue
                
            # If we get here, it's new input
            current_input = user_input
            result_value = calculate(current_input)
            
            if result_value:
                history_entry = f"{current_input} = {result_value}"
                if history_entry not in history:
                    history.append(history_entry)
                current_input = ""
                
                # Limit history size
                if len(history) > 20:
                    history.pop(0)
        
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Check for rofi
    try:
        subprocess.run(["rofi", "-version"], capture_output=True, check=True)
        run_calculator()
    except FileNotFoundError:
        print("Error: rofi not found. Install with: sudo apt install rofi")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting calculator: {e}")
        sys.exit(1)