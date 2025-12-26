# 🐼 Panda — Productivity Assistant Robot

<div align="center">

**A voice-controlled, semi-autonomous robotic assistant designed to enhance daily productivity and accessibility**

[![Competition](https://img.shields.io/badge/Competition-Algerian%20Robotics%202025%2F2026-blue)]()
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()
[![License](https://img.shields.io/badge/License-Competition%20Only-red)]()

[Features](#-key-features) • [Hardware](#-hardware-platform) • [Architecture](#-software-architecture) • [Setup](#-getting-started) • [Team](#-team)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [The Problem We're Solving](#-the-problem-were-solving)
- [Key Features](#-key-features)
- [Competition Context](#-competition-context)
- [Hardware Platform](#-hardware-platform)
- [Software Architecture](#-software-architecture)
- [Safety & Fail-Safe Systems](#-safety--fail-safe-systems)
- [User Interaction](#-user-interaction)
- [Getting Started](#-getting-started)
- [Testing Status](#-testing-status)
- [Known Issues](#-known-issues)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

---

## 🎯 Overview

Panda is a competition-focused, semi-autonomous robotic system that combines physical presence with intelligent voice interaction to help users manage daily tasks, set reminders, and maintain productivity. Built with safety-first principles and a modular architecture, Panda serves as both a practical assistant and an accessibility aid.

### Project Vision

To create an affordable, accessible robotic assistant that helps users overcome organizational challenges and communication barriers through intuitive voice-based interaction and reliable autonomous behavior.

---

## 🔍 The Problem We're Solving

Many young people face significant challenges with:

- **Organization & Time Management**: Difficulty maintaining schedules, remembering tasks, and staying productive
- **Motivation**: Lack of external accountability and reminders
- **Accessibility**: Communication barriers for individuals with speech or hearing difficulties
- **Daily Task Management**: Overwhelming complexity of managing multiple responsibilities

### Our Solution

Panda addresses these challenges through:

✅ **Physical Presence**: A tangible reminder and companion that encourages accountability  
✅ **Voice Interaction**: Natural, hands-free communication for task management  
✅ **Safety-First Design**: Autonomous navigation with comprehensive obstacle avoidance  
✅ **Accessibility Features**: Planned support for sign language and Morse code  
✅ **Intelligent Assistance**: AI-powered responses for complex queries  

---

## ✨ Key Features

### 🎤 Voice Interaction
- Wake-word activation (hands-free operation)
- Multi-command sessions (no repeated wake words)
- Intelligent intent recognition
- Text-to-speech responses
- ChatGPT integration for complex queries

### 🤖 Autonomous Navigation
- Differential drive system (two-wheel control)
- Dual ultrasonic sensors for obstacle detection
- Smart directional avoidance algorithms
- Safe operation in indoor environments

### 🔔 Scheduling & Reminders
- Voice-controlled alarm setting
- Task scheduling with notifications
- Integrated prayer time reminders
- Audio and visual alerts

### 🛡️ Safety Systems
- Gas detection with immediate stop (MQ-9 sensor)
- Obstacle avoidance with dual sensors
- Emergency help button (GPS + email alert)
- Movement toggle for manual control
- Graceful sensor failure handling

### 🌐 Connectivity
- WiFi-enabled (Raspberry Pi)
- Email notifications for emergencies
- SSH access for remote maintenance
- API integration for AI capabilities

### 📱 Display & Feedback
- LED face animations (20 LEDs)
- 16×2 LCD screen for status display
- Audio feedback via speaker
- Real-time state visualization

---

## 🏆 Competition Context

| Detail | Information |
|--------|-------------|
| **Competition** | Algerian Robotics Competition 2025/2026 |
| **Category** | Real-World Problem Solving |
| **Requirements** | Robotic solution addressing a practical challenge |
| **Restrictions** | None specified |
| **Target Environment** | Indoor, flat surfaces, controlled arenas |

---

## 🔧 Hardware Platform

### Main Components

#### Computing
- **Brain**: Raspberry Pi 4 Model B (4GB RAM)
  - Runs Python-based control system
  - Handles sensors, audio, vision, and decision-making
  - WiFi connectivity for API access
  
- **Motor Controller**: Arduino Uno
  - USB-serial communication with Pi
  - L293D Motor Driver Shield
  - Controls 2× TT DC motors
  - Controls camera servo (tilt)

#### Power System
- **Raspberry Pi**: 10,000 mAh power bank
- **Motors**: 4× AA batteries (separate circuit)
- **Estimated Runtime**: TBD (pending full testing)

#### Mechanical Design
- **Body**: Round chassis
- **Drive System**: Two-wheel differential drive
- **Stabilization**: Side-mounted support wheels
- **Camera Mount**: Servo-controlled tilt mechanism

### Sensor Suite

| Sensor | Purpose | Status | Critical |
|--------|---------|--------|----------|
| USB Camera | Person detection, vision | Software tested | No |
| USB Microphone | Voice input (STT) | Software tested | Yes |
| 2× Ultrasonic (HC-SR04) | Obstacle avoidance | Not tested | Yes |
| DHT11 | Temperature & humidity | Not tested | No |
| MQ-9 | Gas detection | Not tested | Yes |
| GPS Module (M6) | Emergency location | Not tested | No |
| 16×2 LCD (I²C) | Status display | Working ✓ | No |
| 20× LEDs | Robot face & feedback | Not tested | No |

### Wiring Overview

```
┌─────────────────┐
│  Raspberry Pi 4 │
│   (Main Brain)  │
└────┬───────┬────┘
     │       │
     │       └──────> USB Camera
     │       └──────> USB Microphone
     │
     ├──────> GPIO → Sensors (DHT11, MQ-9, Ultrasonic)
     ├──────> I²C → LCD Display
     ├──────> GPIO → LED Array
     │
     └──────> USB Serial
                │
         ┌──────▼──────┐
         │ Arduino Uno │
         │  + L293D    │
         └──┬──────┬───┘
            │      │
            │      └──> Servo Motor (Camera Tilt)
            │
            └──> DC Motors (×2)
```

---

## 🏗️ Software Architecture

### Design Principles

1. **Separation of Concerns**: Hardware, logic, and display completely separated
2. **Safety First**: All critical operations fail-safe
3. **Non-Blocking**: Threaded sensor reading and processing
4. **Modular**: Easy to test, maintain, and extend
5. **Laptop-Friendly**: Can run without hardware for development

### System Overview

```
┌───────────────────────────────────────────────────┐
│                    main.py                        │
│            (Entry Point - No Logic)               │
└──────────────────────┬────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌─────▼─────┐  ┌────▼────┐
   │ Sensors │   │   Audio   │  │ Display │
   │ Manager │   │  Pipeline │  │ Manager │
   └────┬────┘   └─────┬─────┘  └────┬────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
              ┌────────▼────────┐
              │ Decision Engine │
              │   (Core Logic)  │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌─────▼─────┐  ┌────▼────┐
   │ Actions │   │ Movement  │  │  State  │
   │ Handler │   │Controller │  │ Manager │
   └─────────┘   └───────────┘  └─────────┘
```

### Directory Structure

```
PI_BRAIN/
│
├── main.py                      # Entry point (orchestration only)
│
├── core/                        # Core logic modules
│   ├── decision_engine.py       # Main decision-making logic
│   ├── actions.py               # Action implementations
│   ├── states.py                # State management
│   ├── movement_controller.py   # Movement coordination
│   └── obstacle_avoidance.py    # Avoidance algorithms
│
├── sensors/                     # Sensor interface layer
│   ├── sensor.py                # Sensor aggregator (threaded)
│   ├── dht11.py                 # Temperature/humidity
│   ├── mq9.py                   # Gas detection
│   ├── gps.py                   # GPS module
│   ├── ultrasonic.py            # Distance sensors
│   └── camera.py                # Vision processing
│
├── audio/                       # Audio processing pipeline
│   ├── audio_receiver.py        # Microphone input handler
│   ├── speech_engine.py         # STT + Intent recognition
│   └── tts.py                   # Text-to-speech output
│
├── display/                     # Output modules
│   ├── leds.py                  # LED control (robot face)
│   └── lcd.py                   # LCD screen interface
│
├── scheduler/                   # Task scheduling
│   └── scheduler.py             # Alarm & reminder system
│
├── config/                      # Configuration
│   └── settings.py              # Constants & parameters
│
├── logs/                        # Logging (planned)
│   └── log_manager.py           # Centralized logging
│
├── tests/                       # Unit tests (planned)
│   ├── test_sensors.py
│   ├── test_movement.py
│   └── test_audio.py
│
├── docs/                        # Additional documentation
│   ├── HARDWARE.md              # Hardware assembly guide
│   ├── API.md                   # Software API documentation
│   └── TROUBLESHOOTING.md       # Common issues & solutions
│
├── requirements.txt             # Python dependencies
├── setup.sh                     # Installation script
└── README.md                    # This file
```

### Key Modules

#### Decision Engine (`core/decision_engine.py`)
The brain of the robot that:
- Processes sensor data
- Evaluates current state
- Determines appropriate actions
- Triggers movement or responses
- Handles emergency situations

#### Sensor Manager (`sensors/sensor.py`)
- Threaded sensor reading (non-blocking)
- Data aggregation and filtering
- Graceful handling of sensor failures
- Provides clean interface to decision engine

#### Audio Pipeline (`audio/`)
- Wake-word detection
- Speech-to-text conversion
- Intent recognition (local + ChatGPT fallback)
- Text-to-speech response generation
- Session management

#### Movement Controller (`core/movement_controller.py`)
- Motor speed control
- Direction management
- Integration with obstacle avoidance
- Emergency stop capability
- Movement enable/disable toggle

---

## 🛡️ Safety & Fail-Safe Systems

### Emergency Stop Conditions

1. **Gas Detection (MQ-9)**
   - Immediate full stop
   - Buzzer activation
   - Voice alert: "Danger! Gas detected!"
   - Movement locked until manual reset

2. **Ultrasonic Sensor Failure**
   - Both sensors non-responsive
   - Alert triggered
   - Reduced speed operation
   - Manual intervention required

3. **Software Crash**
   - Automatic motor stop
   - Alert buzzer
   - Log saved
   - Manual restart required

### Obstacle Avoidance Strategy

```
┌─────────────────────────────────────┐
│  Ultrasonic Sensors (Front L/R)    │
└──────────┬──────────────────────────┘
           │
    ┌──────▼──────┐
    │ Both Clear? │
    └──┬──────┬───┘
       │ Yes  │ No
       │      │
       │   ┌──▼─────────────┐
       │   │ Which blocked? │
       │   └──┬────────┬────┘
       │      │ Left   │ Right
       │      │        │
       │   ┌──▼──┐  ┌──▼──┐
       │   │Turn │  │Turn │
       │   │Right│  │Left │
       │   └─────┘  └─────┘
       │
    ┌──▼──────┐
    │Continue │
    │Forward  │
    └─────────┘
```

**Algorithm**:
- Continuous polling of both sensors
- Distance threshold: 20cm (configurable)
- Turn angle: 45° (configurable)
- Speed reduction during turns
- Re-evaluation after each turn

### Human Override

**Movement Toggle Button**:
- Enables/disables all movement
- Enabled by default on startup
- Immediate effect (no delay)
- Visual feedback on LCD
- Does not affect other functions

**Emergency Help Button**:
- Sends email with GPS coordinates
- Subject: "HELP - Panda Emergency Alert"
- Includes last known location
- Non-blocking operation
- Confirmation beep

---

## 👤 User Interaction

### Voice Commands

**Session Flow**:
1. User says wake word: "Hey Panda"
2. Panda responds: "I'm listening"
3. User gives commands (multiple allowed)
4. Session ends after 10 seconds of silence

**Example Commands**:
- "Set an alarm for 7 AM"
- "Remind me to study at 3 PM"
- "What's the temperature?"
- "Move forward"
- "Stop moving"
- "Play prayer time reminder"

### Physical Buttons

| Button | Function | Behavior |
|--------|----------|----------|
| **Help** | Emergency alert | Sends GPS location via email |
| **Movement Toggle** | Enable/disable movement | Immediate stop/start |

### Planned Interactions

- **Sign Language Recognition**: Using camera + ML model
- **Morse Code Input**: Via button presses or audio
- **Mobile App**: Remote control and monitoring (future)

---

## 🚀 Getting Started

### Prerequisites

**Hardware**:
- Raspberry Pi 4 (4GB RAM recommended)
- Arduino Uno + L293D Shield
- Sensors as listed in hardware section
- Assembled chassis with motors

**Software**:
- Raspberry Pi OS (Bullseye or later)
- Python 3.9+
- Arduino IDE (for motor controller upload)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AmpleVoice/Productivity-Asistant-robot.git
   cd Productivity-Asistant-robot/PI_BRAIN
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Settings**
   ```bash
   cp config/settings.example.py config/settings.py
   # Edit settings.py with your API keys and preferences
   ```

4. **Upload Arduino Code**
   - Open `arduino/motor_controller.ino` in Arduino IDE
   - Upload to Arduino Uno

5. **Test Hardware**
   ```bash
   python tests/hardware_test.py
   ```

6. **Run Panda**
   ```bash
   python main.py
   ```

### Configuration

Edit `config/settings.py` to customize:
- Sensor pins and thresholds
- API keys (ChatGPT, TTS service)
- Email credentials for alerts
- Movement parameters
- Audio settings

---

## 🧪 Testing Status

### ✅ Tested & Working
- LCD Display (I²C communication)
- Speech-to-text (software level)
- Basic logic flow

### ⚠️ Software Tested, Hardware Pending
- Camera person detection
- Text-to-speech output
- Intent recognition

### ❌ Not Yet Tested
- Motor control system
- Ultrasonic sensors
- DHT11 sensor
- MQ-9 gas sensor
- GPS module
- LED array (power consumption concern)
- Full system integration

### 📊 Performance Benchmarks
**Status**: Not yet conducted

**Planned Tests**:
- Boot time to ready state
- Command response latency
- Battery life under typical use
- Sensor polling frequency
- CPU/memory usage
- WiFi stability

---

## ⚠️ Known Issues

### Critical
1. **Heavy Internet Dependency**
   - ChatGPT API required for unknown intents
   - TTS service requires connection
   - No offline fallback mode

2. **Untested Motor Power**
   - 4× AA batteries may be insufficient
   - Current draw not measured
   - Runtime unknown

### Important
3. **LED Power Consumption**
   - 20 LEDs may drain power quickly
   - No power monitoring implemented

4. **Performance Unknown**
   - No benchmarking conducted
   - Latency not measured
   - Resource usage not profiled

### Minor
5. **Limited Error Recovery**
   - Some failures require manual restart
   - No automatic recovery mechanisms

6. **No Centralized Logging**
   - Debugging difficult
   - Issue tracking incomplete

---

## 🗺️ Roadmap

### Phase 1: Competition Preparation (Current)
- [ ] Complete hardware integration testing
- [ ] Validate all sensors
- [ ] Test full system with battery power
- [ ] Optimize response latency
- [ ] Create demo scenarios
- [ ] Prepare presentation materials

### Phase 2: Post-Competition (Q2 2026)
- [ ] Implement offline operation mode
- [ ] Add power monitoring and alerts
- [ ] Optimize performance and reduce latency
- [ ] Expand built-in knowledge base
- [ ] Implement centralized logging system
- [ ] Add active cooling for Raspberry Pi
- [ ] Configure automatic startup on boot

### Phase 3: Feature Expansion (Future)
- [ ] Sign language recognition
- [ ] Morse code interaction
- [ ] Mobile app for remote control
- [ ] Multiple language support (Arabic, French)
- [ ] Advanced scheduling features
- [ ] Integration with smart home devices
- [ ] Computer vision improvements

### Phase 4: Community & Scale (Long-term)
- [ ] Open-source hardware designs
- [ ] Assembly instructions and tutorials
- [ ] Cost optimization (target: under $150)
- [ ] Educational curriculum integration
- [ ] Accessibility features for diverse needs

---

## 🤝 Contributing

This project is currently maintained for competition purposes. After the Algerian Robotics Competition 2025/2026, we plan to open it for community contributions.

**Want to help?**
- Report bugs via GitHub Issues
- Suggest features in Discussions
- Share your ideas for improvements
- Star the repository to show support

**Post-Competition**:
We'll establish contribution guidelines and welcome pull requests for:
- New features
- Bug fixes
- Documentation improvements
- Hardware optimizations
- Test coverage

---

## 👥 Team

### DTA Team (non-official)

**Team Members**:

🧑‍💻 **Mohamed Alaa Eddine KHELIFI**  
*Lead Developer & Project Manager*  
Primary repository maintainer, software architecture, system integration

🔧 **Hakim Taher AIT SAID**  
*Hardware Specialist*  
Mechanical design, electronics assembly, sensor integration

🤖 **Rostom Mohamed Kamel BOUABDELLAH**  
*AI & Algorithms*  
Decision engine logic, obstacle avoidance, voice processing

---

**Institution**: Math High School Kouba  
**Specialization**: Mathematics Stream — 2nd Year of Secondary School  
**Location**: Algeria  
**Project Year**: 2025 – 2026

---

## 📄 License

This project is developed for the **Algerian Robotics Competition 2025/2026**.

**Current Status**: Competition Only  
**Post-Competition**: To be determined (likely open-source)

---

## 📞 Contact & Links

- **GitHub**: [Productivity-Assistant-robot](https://github.com/AmpleVoice/Productivity-Asistant-robot)
- **Issues**: [Report a Bug](https://github.com/AmpleVoice/Productivity-Asistant-robot/issues)
- **Discussions**: [Join the Conversation](https://github.com/AmpleVoice/Productivity-Asistant-robot/discussions)

---

## 🙏 Acknowledgments

Special thanks to:
- Math High School Kouba for supporting our project
- The Algerian Robotics Competition organizers
- The open-source community for tools and libraries
- Our families and teachers for their encouragement

---

<div align="center">

**Built with 💚 by DTA Team**

*Empowering productivity, one voice command at a time*

</div>