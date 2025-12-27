"""
startup.py - System orchestration and hardware validation.

Responsibilities:
- Initialize hardware backends (GPIO, serial, I2C)
- Validate all hardware components
- Start subsystems in correct order
- Run main control loop
- Clean shutdown

NOT responsible for:
- Direct GPIO pin manipulation (uses sensor interface)
- Behavior-level actions (uses test helpers only)
- Guessing sensor schemas (trusts stable schema)
"""

import sys
import os
import signal
import time

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import settings
from core.states import RobotState
from sensors.sensor import RobotSensors
from core.decision_engine import DecisionEngine
from core import actions
from vision.vision_engine import VisionEngine
from camera.camera_manager import CameraManager


class HardwareValidator:
    """Validates all robot hardware before startup."""
    
    def __init__(self):
        self.results = {
            "camera": False,
            "microphone": False,
            "speaker": False,
            "lcd": False,
            "ultrasonic": False,
            "dht11": False,
            "mq9": False,
            "gps": False,
            "orientation": False
        }
        self.critical_failed = []
        self.optional_failed = []
    
    def validate_all(self, sensors):
        """
        Run complete hardware validation.
        
        Args:
            sensors: RobotSensors instance with stable schema
        
        Returns:
            bool: True if all CRITICAL components pass
        """
        print("\n" + "=" * 60)
        print("🔍 HARDWARE VALIDATION")
        print("=" * 60)
        
        # Define critical vs optional components
        critical = ["camera", "microphone", "speaker", "ultrasonic", "orientation"]
        
        # Run all checks
        self._check_orientation(sensors)
        self._check_camera()
        self._check_microphone()
        self._check_speaker()
        self._check_lcd()
        self._check_sensors(sensors)
        
        # Analyze results
        print("\n" + "-" * 60)
        print("📊 VALIDATION RESULTS:")
        print("-" * 60)
        
        for component, status in self.results.items():
            is_critical = component in critical
            symbol = "✓" if status else "✗"
            priority = "[CRITICAL]" if is_critical else "[OPTIONAL]"
            
            print(f"{symbol} {component.upper():15} {priority:12} {'PASS' if status else 'FAIL'}")
            
            if not status:
                if is_critical:
                    self.critical_failed.append(component)
                else:
                    self.optional_failed.append(component)
        
        print("-" * 60)
        
        # Summary
        if self.critical_failed:
            print(f"\n✗ CRITICAL FAILURES: {', '.join(self.critical_failed)}")
            print("❌ System CANNOT start - fix critical components first")
            return False
        
        if self.optional_failed:
            print(f"\n⚠ OPTIONAL FAILURES: {', '.join(self.optional_failed)}")
            print("⚠ System can start but with reduced functionality")
        else:
            print("\n✓ ALL SYSTEMS NOMINAL")
        
        return True
    
    def _check_orientation(self, sensors):
        """
        Check if robot is upside down using sensor interface.
        
        This uses the stable sensor schema - NO direct GPIO access.
        """
        print("\n[1/9] Checking orientation...")
        
        try:
            sensor_data = sensors.read()
            orientation = sensor_data.get("orientation", {})
            
            if not orientation.get("available"):
                print("  ⚠ Orientation sensor not available (assuming correct)")
                self.results["orientation"] = True
                return
            
            is_flipped = orientation.get("flipped", False)
            
            if is_flipped:
                print("  ✗ Robot is UPSIDE DOWN!")
                print("  → Please flip the robot right-side up")
                self.results["orientation"] = False
            else:
                print("  ✓ Orientation correct")
                self.results["orientation"] = True
                
        except Exception as e:
            print(f"  ✗ Orientation check failed: {e}")
            self.results["orientation"] = False
    
    def _check_camera(self):
        """Check camera functionality."""
        print("\n[2/9] Checking camera...")
        try:
            cam = CameraManager()
            frame = cam.read_frame()
            cam.release()
            
            if frame is not None and frame.size > 0:
                print(f"  ✓ Camera working (resolution: {frame.shape[1]}x{frame.shape[0]})")
                self.results["camera"] = True
            else:
                print("  ✗ Camera returned empty frame")
                self.results["camera"] = False
                
        except Exception as e:
            print(f"  ✗ Camera failed: {e}")
            self.results["camera"] = False
    
    def _check_microphone(self):
        """Check microphone functionality."""
        print("\n[3/9] Checking microphone...")
        try:
            import pyaudio
            
            p = pyaudio.PyAudio()
            
            # Try to open microphone stream
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            
            # Read a small audio chunk
            data = stream.read(1024, exception_on_overflow=False)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            if data:
                print("  ✓ Microphone working")
                self.results["microphone"] = True
            else:
                print("  ✗ Microphone returned no data")
                self.results["microphone"] = False
                
        except Exception as e:
            print(f"  ✗ Microphone failed: {e}")
            self.results["microphone"] = False
    
    def _check_speaker(self):
        """Check speaker functionality using test helper."""
        print("\n[4/9] Checking speaker...")
        try:
            # Use minimal test helper - NOT behavior-level action
            actions.hardware_test_beep()
            time.sleep(0.2)
            
            print("  ✓ Speaker working (test beep played)")
            self.results["speaker"] = True
            
        except Exception as e:
            print(f"  ✗ Speaker failed: {e}")
            self.results["speaker"] = False
    
    def _check_lcd(self):
        """Check LCD screen functionality using test helper."""
        print("\n[5/9] Checking LCD screen...")
        try:
            # Use minimal test helper - NOT behavior-level action
            actions.hardware_test_lcd()
            
            print("  ✓ LCD screen working")
            self.results["lcd"] = True
            
        except Exception as e:
            print(f"  ✗ LCD failed: {e}")
            self.results["lcd"] = False
    
    def _check_sensors(self, sensors):
        """
        Check all sensor modules using stable schema.
        
        This trusts the sensor interface - NO schema guessing.
        """
        if not sensors:
            print("\n[6-9/9] ✗ Sensor interface not available")
            self.results["ultrasonic"] = False
            self.results["dht11"] = False
            self.results["mq9"] = False
            self.results["gps"] = False
            return
        
        try:
            # Read using STABLE schema
            sensor_data = sensors.read()
            
            # Check Ultrasonic sensors
            print("\n[6/9] Checking ultrasonic sensors...")
            ultrasonic = sensor_data.get("ultrasonic", {})
            left = ultrasonic.get("left")
            right = ultrasonic.get("right")
            
            if left is not None and right is not None:
                if 2 <= left <= 400 and 2 <= right <= 400:
                    print(f"  ✓ Ultrasonic sensors working (L: {left:.1f}cm, R: {right:.1f}cm)")
                    self.results["ultrasonic"] = True
                else:
                    print(f"  ⚠ Ultrasonic readings out of range (L: {left}, R: {right})")
                    self.results["ultrasonic"] = False
            else:
                print("  ✗ Ultrasonic sensors returned None")
                self.results["ultrasonic"] = False
            
            # Check DHT11 (temperature/humidity)
            print("\n[7/9] Checking DHT11 sensor...")
            dht = sensor_data.get("dht11", {})
            temp = dht.get("temperature_c")
            humidity = dht.get("humidity")
            
            if temp is not None and humidity is not None:
                print(f"  ✓ DHT11 working (Temp: {temp:.1f}°C, Humidity: {humidity:.1f}%)")
                self.results["dht11"] = True
            else:
                print("  ⚠ DHT11 failed to read")
                self.results["dht11"] = False
            
            # Check MQ9 (gas sensor)
            print("\n[8/9] Checking MQ9 gas sensor...")
            mq9 = sensor_data.get("mq9", {})
            co_ppm = mq9.get("co_ppm")
            dangerous = mq9.get("dangerous", False)
            
            if co_ppm is not None:
                status = "⚠ DANGEROUS!" if dangerous else "✓ Safe"
                print(f"  ✓ MQ9 working (CO: {co_ppm:.1f} ppm) {status}")
                self.results["mq9"] = True
            else:
                print("  ⚠ MQ9 failed to read")
                self.results["mq9"] = False
            
            # Check GPS
            print("\n[9/9] Checking GPS module...")
            gps = sensor_data.get("gps", {})
            lat = gps.get("latitude")
            lon = gps.get("longitude")
            has_fix = gps.get("fix", False)
            
            if has_fix and lat is not None and lon is not None:
                print(f"  ✓ GPS working (Lat: {lat:.6f}, Lon: {lon:.6f})")
                self.results["gps"] = True
            else:
                print("  ⚠ GPS no fix (may need clear sky)")
                self.results["gps"] = False
                
        except Exception as e:
            print(f"  ✗ Sensor check failed: {e}")
            import traceback
            traceback.print_exc()
            self.results["ultrasonic"] = False
            self.results["dht11"] = False
            self.results["mq9"] = False
            self.results["gps"] = False


class RobotSystem:
    """Main robot system coordinator."""
    
    def __init__(self):
        self.sensors = None
        self.vision = None
        self.decision = None
        self.audio = None
        self.running = False
        self._shutdown_requested = False
        
    def initialize(self):
        """Initialize and validate all robot subsystems."""
        print("=" * 60)
        print("🤖 ROBOT SYSTEM INITIALIZATION")
        print("=" * 60)
        
        # Step 1: Initialize GPIO backend (single owner)
        print("\n⚡ Initializing GPIO backend...")
        try:
            self._initialize_gpio()
            print("✓ GPIO backend ready")
        except Exception as e:
            print(f"✗ GPIO initialization failed: {e}")
            return False
        
        # Step 2: Initialize sensor interface
        print("\n📡 Initializing sensor interface...")
        try:
            self.sensors = RobotSensors()
            print("✓ Sensor interface ready")
        except Exception as e:
            print(f"✗ Sensor interface failed: {e}")
            return False
        
        # Step 3: Hardware validation
        validator = HardwareValidator()
        if not validator.validate_all(self.sensors):
            return False
        
        # Step 4: Initialize vision system
        print("\n" + "=" * 60)
        print("📷 Initializing vision system...")
        print("=" * 60)
        try:
            self.vision = VisionEngine()
            self.vision.start()
            
            if not self.vision.wait_ready(timeout=5):
                print("⚠ Vision system not ready within timeout — continuing with degraded vision")
            else:
                print("✓ Vision system ready")
            
        except Exception as e:
            print(f"✗ Vision initialization failed: {e}")
            return False

        # Step 5: Initialize decision engine
        print("\n" + "=" * 60)
        print("🧠 Initializing decision engine...")
        print("=" * 60)
        try:
            self.decision = DecisionEngine(
                sensors=self.sensors,
                vision=self.vision
            )
            
            # Set initial state to IDLE
            self.decision.state = RobotState.IDLE
            print(f"✓ Decision engine ready (State: {self.decision.state.name})")
            
        except Exception as e:
            print(f"✗ Decision engine failed: {e}")
            return False

        # Step 6: Initialize audio manager (last - depends on decision engine)
        print("\n" + "=" * 60)
        print("🎤 Initializing audio manager...")
        print("=" * 60)
        try:
            from audio.audio_manager import AudioManager
            self.audio = AudioManager(self.decision)
            self.audio.start_async()
            print("✓ Audio manager started")
        except Exception as e:
            print(f"⚠ Audio manager failed to start: {e}")
            print("  (Continuing without voice control)")
            self.audio = None
        
        # Success
        print("\n" + "=" * 60)
        print("✅ ALL SYSTEMS READY")
        print("=" * 60)
        
        # Display sensor status summary
        self._display_sensor_summary(validator.results)
        
        return True
    
    def _initialize_gpio(self):
        """
        Initialize GPIO backend (single owner).
        
        This is the ONLY place where GPIO.setmode() is called.
        All other modules receive configured GPIO objects.
        """
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except Exception:
            # Fall back to mock GPIO if available
            import sys
            dm = sys.modules.get('dev_mocks')
            if dm and getattr(dm, 'gpio', None):
                GPIO = dm.gpio
                print("  ⚠ Using mock GPIO (dev_mocks)")
            else:
                raise RuntimeError("No GPIO backend available")
    
    def _display_sensor_summary(self, results):
        """Display final sensor status summary."""
        print("\n📊 SENSOR STATUS SUMMARY:")
        print("-" * 60)
        
        categories = {
            "CRITICAL SYSTEMS": ["camera", "microphone", "speaker", "ultrasonic", "orientation"],
            "OPTIONAL SENSORS": ["lcd", "dht11", "mq9", "gps"]
        }
        
        for category, sensors in categories.items():
            print(f"\n{category}:")
            for sensor in sensors:
                status = "✓ ONLINE" if results.get(sensor) else "✗ OFFLINE"
                print(f"  • {sensor.upper():15} {status}")
        
        print("-" * 60)
    
    def run(self):
        """Main control loop."""
        self.running = True
        
        print("\n" + "=" * 60)
        print("🚀 STARTING MAIN CONTROL LOOP")
        print("=" * 60)
        print("State: IDLE")
        print("Press Ctrl+C to stop")
        print("-" * 60 + "\n")
        
        try:
            while self.running and not self._shutdown_requested:
                # Main decision cycle
                self.decision.update()
                
                # Control loop timing (20Hz)
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n\n⚠ Keyboard interrupt detected")
        except Exception as e:
            print(f"\n\n✗ Fatal error in main loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of all systems."""
        if self._shutdown_requested:
            return  # Prevent double shutdown
        
        self._shutdown_requested = True
        
        print("\n" + "=" * 60)
        print("🛑 SHUTTING DOWN SYSTEM")
        print("=" * 60)
        
        self.running = False
        
        # Stop audio manager
        if self.audio:
            print("• Stopping audio manager...")
            try:
                self.audio.stop()
            except Exception as e:
                print(f"  ⚠ Audio shutdown error: {e}")
        
        # Stop vision
        if self.vision:
            print("• Stopping vision system...")
            try:
                self.vision.stop()
                self.vision.join(timeout=2)
            except Exception as e:
                print(f"  ⚠ Vision shutdown error: {e}")
        
        # Stop motors (safe state)
        print("• Stopping motors...")
        try:
            actions.motors_stop()
        except Exception as e:
            print(f"  ⚠ Motor stop error: {e}")
        
        # Clear LCD
        print("• Clearing LCD...")
        try:
            actions.lcd_clear()
        except Exception as e:
            print(f"  ⚠ LCD clear error: {e}")
        
        # Cleanup sensors
        if self.sensors:
            print("• Cleaning up sensors...")
            try:
                self.sensors.cleanup()
            except Exception as e:
                print(f"  ⚠ Sensor cleanup error: {e}")
        
        # GPIO cleanup (we are the single owner)
        print("• Cleaning up GPIO...")
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except Exception:
            pass
        
        print("\n✓ Shutdown complete")
        print("=" * 60)


# Global robot instance for signal handler
_robot_instance = None


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global _robot_instance
    if _robot_instance:
        _robot_instance.shutdown()
    sys.exit(0)


def main():
    """Main entry point."""
    global _robot_instance
    
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create robot system
    robot = RobotSystem()
    _robot_instance = robot
    
    # Initialize with hardware validation
    if not robot.initialize():
        print("\n" + "=" * 60)
        print("❌ INITIALIZATION FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above and try again.")
        sys.exit(1)
    
    # Run main loop
    robot.run()
    
    sys.exit(0)


if __name__ == "__main__":
    main()