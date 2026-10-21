# Pošta Srbije Tracking for Home Assistant

A custom Home Assistant integration to track packages via **Pošta Srbije** (`posta.rs`), fully compatible with **HACS**.

---

## Installation

### Via HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Paste your GitHub repository URL (`https://github.com/vlatko019/ha-posta-srbije`).
4. Select category: **Integration**.
5. Click **Add**, then find **Pošta Srbije Tracking** in the list, download it, and restart Home Assistant.

### Manual Installation
1. Copy the `custom_components/posta_srbije` directory into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.

---

## Configuration
1. Go to **Settings** -> **Devices & Services** -> **Add Integration**.
2. Search for **Pošta Srbije Tracking**.
3. Enter your tracking number and an optional friendly name.

---

## Features
- Tracks international and domestic postal numbers (e.g., `LR...NL`).
- Exposes the latest shipment status as the sensor state.
- Provides attributes including `last_location`, `last_update`, and full tracking event `history`.