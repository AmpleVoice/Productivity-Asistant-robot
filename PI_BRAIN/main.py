#!/usr/bin/env python3
"""
Single entry point for the robot application.
Provides simple CLI flags useful for development and testing:
  --no-hw-check  : Skip hardware validation (dev)
  --no-vision    : Disable vision subsystem (dev)
  --debug        : Enable debug logging

This file keeps changes lightweight by monkey-patching startup behavior when needed
so we don't have to modify the existing startup flow more than necessary.
"""

import argparse
import logging
import os
import sys

# Ensure project root is on sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# On non-Pi platforms, install dev mocks for GPIO/DHT/serial when RPi.GPIO is not present
try:
    import RPi.GPIO  # type: ignore
except Exception:
    try:
        import dev_mocks
        # Avoid overriding real audio drivers on desktop; keep use_audio=False so microphone/speaker work
        dev_mocks.install_mocks(use_audio=False)
        print("[main] dev_mocks installed (no audio) for non-Pi platform")
    except Exception as e:
        print(f"[main] failed to install dev_mocks: {e}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="PI_BRAIN robot main entrypoint")
    parser.add_argument("--no-hw-check", action="store_true", help="Skip hardware validation (dev)")
    parser.add_argument("--no-vision", action="store_true", help="Disable vision subsystem (dev)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format="[%(levelname)s] %(message)s")

    logging.info("Starting PI_BRAIN (main entrypoint)")

    # Import here so sys.path is already configured
    try:
        import startup.startup as startup
    except Exception as e:
        logging.error("Failed to import startup module: %s", e)
        raise

    # Option: skip hardware checks by replacing HardwareValidator.validate_all
    if args.no_hw_check:
        logging.info("--no-hw-check: hardware validation will be skipped")

        def _always_ok(self, sensors):
            logging.debug("Hardware validation skipped (no-hw-check)")
            return True

        try:
            startup.HardwareValidator.validate_all = _always_ok
        except Exception:
            logging.warning("Could not patch HardwareValidator; continuing anyway")

    # Option: disable vision by patching VisionEngine with a minimal stub
    if args.no_vision:
        logging.info("--no-vision: vision subsystem disabled (stub)")

        class DummyVisionEngine:
            def __init__(self):
                self._running = False

            def start(self):
                self._running = True

            def stop(self):
                self._running = False

            def join(self, timeout=None):
                return

            def wait_ready(self, timeout=None):
                return True

            def get_target(self):
                return {"center": None, "width": None}

        try:
            startup.VisionEngine = DummyVisionEngine
        except Exception:
            logging.warning("Could not patch VisionEngine; continuing anyway")

    # Run startup main (it will register its own signal handler and perform initialize + run)
    try:
        startup.main()
    except SystemExit as se:
        # Propagate clean exits
        logging.info("Exiting: %s", se)
        raise
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.exception("Unhandled exception in main: %s", e)
        raise


if __name__ == "__main__":
    main()
