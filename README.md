---

# BUCROCCS Monitor - Real-Time Data Display for Sensor Monitoring

This project is a monitoring tool that retrieves data from a UDP server and displays real-time sensor data using a graphical interface built with Flet. It visually represents humidity, temperature, light, and moisture levels for each hour of the day. It is designed to work in conjunction with the BUCROCCS system, particularly for monitoring sensor data sent via UDP.

## Requirements

- Python 3.x
- Flet (`flet`)
- asyncio

### Python Libraries

To install the necessary libraries, run the following command:

```bash
pip install -r requirements.txt
```

Where `requirements.txt` includes:
```
flet
asyncio
```

## Overview

This project provides a graphical interface that:
- Displays real-time data retrieved from a UDP server.
- Shows sensor values for each hour of the selected day (humidity, temperature, light, and moisture).
- Visualizes whether the pump and light were activated at specific times.

The data is periodically fetched from the UDP server, and the interface updates every few seconds to reflect changes in sensor values.

### Main Components

1. **main.py**
   - The main entry point for the monitoring tool.
   - Retrieves data from the UDP server and displays it in a user-friendly format using the Flet framework.
   - The interface includes a tab to select the day of the week and a progress bar showing the refresh status.
   - Data displayed includes:
     - Time of the reading.
     - Humidity percentage.
     - Temperature in Celsius.
     - Light intensity percentage.
     - Moisture percentage.
     - Light state (On/Off).
     - Pump state (On/Off).
     - Whether the pump was activated in the current hour.

2. **UdpClient.py**
   - Handles communication with a remote UDP server.
   - Retrieves sensor data asynchronously via the UDP protocol.
   - Ensures non-blocking communication using asyncio.

3. **Helpers.py**
   - Provides utility functions for handling time-related operations, such as getting the current hour or day of the week.
   - Includes functions to convert the current day into an integer or retrieve the name of the day based on the index.

### How to Run

1. Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python main.py
```

This will start the graphical monitoring tool. The application will connect to the UDP server (defined in `UdpClient`) and start displaying real-time sensor data for the current day.

### Example Usage

Once the application is running, you can:
- Select the day of the week using the tabs at the top of the interface.
- View real-time data updates every few seconds, with the progress bar indicating the time left until the next update.
- Check values such as humidity, temperature, light, and moisture, along with the states of the light and pump.

### Folder Structure

- **main.py**: The main application file that initializes the graphical interface and updates it with real-time data.
- **UdpClient.py**: Manages UDP communication, sending requests and receiving data from the UDP server.
- **Helpers.py**: Provides time-related helper functions, such as retrieving the current hour or day of the week.

### Data Representation

- **Humidity**: Displayed as a percentage.
- **Temperature**: Displayed in degrees Celsius.
- **Light**: Displayed as a percentage of light intensity.
- **Moisture**: Displayed as a percentage.
- **Light Activated**: Indicates whether the light is on (green) or off (red).
- **Pump Activated**: Indicates whether the pump is on (green) or off (red).
- **Pump Activated This Hour**: Shows if the pump was activated within the current hour.

## Extending the System

- You can modify `UdpClient.py` to change the UDP server's IP or port or adjust the data retrieval mechanism.
- Customize the data display in `main.py` by adding new sensor types or altering the layout for additional information.
- Add new days or modify the existing day selection by extending the logic in `Helpers.py`.

---
