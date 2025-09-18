#!/usr/bin/env python3
import subprocess
import math
import sys
import os
import re
from pathlib import Path

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    print("Warning: pyperclip not installed. Install with: pip install pyperclip")

# Persistent history storage
HISTORY_FILE = Path.home() / ".calc_history"
history = []

def load_history():
    """Load history from file"""
    global history
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = [line.strip() for line in f.readlines() if line.strip()]
        except:
            history = []

def save_history():
    """Save history to file"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            for entry in history:
                f.write(entry + '\n')
    except:
        pass

def copy_to_clipboard(text):
    """Copy text to clipboard using pyperclip or fallback methods"""
    text_str = str(text)
    
    # Try pyperclip first
    if PYPERCLIP_AVAILABLE:
        try:
            pyperclip.copy(text_str)
            return True
        except Exception as e:
            print(f"pyperclip error: {e}")
    
    # Fallback to subprocess methods
    clipboard_commands = [
        ['xclip', '-selection', 'clipboard'],
        ['xsel', '--clipboard'],
        ['wl-copy'],
        ['pbcopy']  # For macOS
    ]
    
    for cmd in clipboard_commands:
        try:
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)
            process.communicate(input=text_str)
            if process.returncode == 0:
                return True
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    
    return False

def show_notification(message, urgency="normal"):
    """Show a desktop notification"""
    try:
        subprocess.run([
            "notify-send", 
            "-a", "Calculator",
            "-u", urgency,
            "-t", "2000",
            "Calculator",
            message
        ], check=True)
    except:
        # Fallback to terminal output if notify-send fails
        print(f"📋 {message}")

def preprocess_expression(expr):
    """Preprocess expression to handle implicit multiplication"""
    # Remove spaces
    expr = expr.replace(' ', '')
    
    # Handle implicit multiplication around parentheses
    # Patterns: number(, )(, )number, )(, etc.
    
    # Add * between number and ( e.g., 7( -> 7*(
    expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
    
    # Add * between ) and number e.g., )7 -> )*7
    expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
    
    # Add * between ) and ( e.g., )( -> )*(
    expr = re.sub(r'(\))(\()', r'\1*\2', expr)
    
    # Add * between number and function e.g., 2sqrt -> 2*sqrt
    math_functions = ['sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'exp', 'abs']
    for func in math_functions:
        expr = re.sub(r'(\d)(' + func + r')', r'\1*\2', expr)
    
    # Replace common symbols
    expr = expr.replace('×', '*').replace('÷', '/')
    expr = expr.replace('^', '**')  # Handle exponent notation
    
    return expr

def calculate(expr):
    """Safely calculate mathematical expressions with implicit multiplication support"""
    try:
        expr = expr.strip()
        if not expr:
            return None
        
        # Preprocess the expression to handle implicit multiplication
        expr = preprocess_expression(expr)
        print(f"Processed expression: {expr}")
        
        # Allow math functions and basic operations
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed.update({
            'abs': abs, 'round': round, 'min': min, 'max': max, 'pow': pow,
            'ln': math.log, 'log10': math.log10, 'log': math.log10
        })
        
        result = eval(expr, {"__builtins__": {}}, allowed)
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            elif abs(result) < 1e-10:
                return "0"
            else:
                # Remove trailing .0 for whole numbers
                formatted = f"{result:.10g}"
                if '.' in formatted and formatted.endswith('.0'):
                    return formatted[:-2]
                return formatted
        return str(result)
    except Exception as e:
        print(f"Calculation error: {e}")
        return None

def run_calculator():
    """Simple working calculator"""
    print("Starting calculator...")
    print("Supports implicit multiplication: 2(3+4) = 2*(3+4), 3sqrt(9) = 3*sqrt(9)")
    
    while True:
        try:
            # Build simple display
            display_lines = []
            display_lines.append("Enter calculation (2+2, 7(12*54), sqrt(16), etc.)")
            
            if history:
                display_lines.append("")
                display_lines.append("--- History ---")
                # Show last 6 calculations
                for item in reversed(history[-6:]):
                    display_lines.append(item)
            
            display_text = "\n".join(display_lines)
            
            # Run rofi
            cmd = [
                "rofi",
                "-dmenu",
                "-p", "➤ Calculate:",
                "-theme", "Adapta-Nokto",
                "-lines", "10",
                "-width", "60",
                "-i",
                "-format", "s"
            ]
            
            result = subprocess.run(
                cmd,
                input=display_text,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 1:  # User pressed Escape
                print("Calculator closed by user")
                break
            elif result.returncode != 0:
                print(f"Rofi error: {result.returncode}")
                if result.stderr:
                    print(f"Error output: {result.stderr}")
                break
                
            user_input = result.stdout.strip()
            print(f"User input: '{user_input}'")
            
            # Skip empty input or instructions
            if (not user_input or 
                user_input.startswith("Enter calculation") or 
                user_input == "--- History ---"):
                continue
            
            # Handle history selection
            is_history_selection = False
            for history_item in history:
                if user_input == history_item:
                    is_history_selection = True
                    break
            
            if is_history_selection:
                # This is a history item - copy the result
                if ' = ' in user_input:
                    expr, result_value = user_input.split(' = ', 1)
                    if copy_to_clipboard(result_value):
                        show_notification(f"📋 Copied to clipboard: {result_value}")
                        print(f"✓ COPIED FROM HISTORY: {result_value}")
                    else:
                        show_notification(f"❌ Copy failed: {result_value}", "critical")
                        print(f"Result from history: {result_value}")
                    continue
            
            # Calculate new expression
            result_value = calculate(user_input)
            
            if result_value is not None:
                result_display = f"{user_input} = {result_value}"
                print(f"✅ CALCULATION RESULT: {result_display}")
                
                # Add to history
                history_entry = result_display
                if history_entry not in history:
                    history.append(history_entry)
                    save_history()
                    
                    # Limit history size
                    if len(history) > 15:
                        history.pop(0)
                        save_history()
                
                # Copy to clipboard and show notification
                if copy_to_clipboard(result_value):
                    show_notification(f"📋 Result copied: {result_value}")
                    print(f"✓ COPIED TO CLIPBOARD: {result_value}")
                else:
                    show_notification(f"❌ Copy failed: {result_value}", "critical")
                    print(f"Result (copy failed): {result_value}")
                    
            else:
                error_msg = f"Invalid expression: {user_input}"
                show_notification(error_msg, "critical")
                print(f"❌ {error_msg}")
                    
        except KeyboardInterrupt:
            print("Calculator interrupted")
            break
        except Exception as e:
            print(f"Error in calculator loop: {e}")
            import traceback
            traceback.print_exc()
            break

if __name__ == "__main__":
    print("Calculator starting...")
    print("Now supports implicit multiplication: 2(3+4), 3sqrt(9), etc.")
    
    if not PYPERCLIP_AVAILABLE:
        print("Note: pyperclip not available. Clipboard functionality may be limited.")
        print("Install with: pip install pyperclip")
    
    # Load history
    load_history()
    print(f"Loaded {len(history)} history items")
    
    # Check for rofi
    try:
        result = subprocess.run(["rofi", "-version"], capture_output=True, check=True)
        print(f"Rofi found: {result.stdout.decode().strip()}")
    except FileNotFoundError:
        print("Error: rofi not found. Install with: sudo apt install rofi")
        sys.exit(1)
    except Exception as e:
        print(f"Error checking rofi: {e}")
        sys.exit(1)
    
    # Check for notify-send
    try:
        subprocess.run(["notify-send", "--version"], capture_output=True, check=True)
        print("Desktop notifications available")
    except:
        print("Desktop notifications not available (install libnotify-bin)")
    
    # Run calculator
    try:
        run_calculator()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)