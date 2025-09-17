# Rofi Quick Calc

A lightweight, rofi-based calculator with calculation history.

## Features

-   **Persistent history**: Your calculation history remains visible while typing
-   **Math functions**: Supports `sin`, `cos`, `tan`, `log`, `sqrt`, and other math operations
-   **Lightweight**: Runs entirely through rofi with no external dependencies

## Installation

1. Ensure you have `rofi` installed:

    ```bash
    sudo apt install rofi  # Debian/Ubuntu
    ```

    ```bash
    sudo pacman -S rofi  # Arch
    ```

2. Make the script executable:

    ```bash
    chmod +x rofi-quick-calc.py
    ```

3. (Optional) Move to your PATH:
    ```bash
    sudo mv rofi-quick-calc.py /usr/local/bin/rofi-quick-calc
    ```

## Usage

Run the script:

```bash
./rofi-quick-calc.py
```

Or if moved to PATH:

```bash
rofi-quick-calc
```

## Key Features

-   **Type mathematical expressions** in the input field
-   **Press Enter** to calculate and add to history
-   **Escape** to exit

## Supported Operations

-   Basic arithmetic: `+`, `-`, `*`, `/`, `**` (power)
-   Math functions: `sin()`, `cos()`, `tan()`, `log()`, `sqrt()`, etc.
-   Constants: `pi`, `e`
-   Advanced: `abs()`, `round()`, `min()`, `max()`, `pow()`

## Examples

-   `2 + 2 * 3`
-   `sin(pi/2)`
-   `sqrt(16) + log(100)`
-   `2**8 + 45/3`

