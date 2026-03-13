import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def list_serial_ports() -> List[str]:
    try:
        from serial.tools import list_ports  # type: ignore

        ports = [p.device for p in list_ports.comports() if getattr(p, "device", None)]
        ports = [p for p in ports if isinstance(p, str) and p]
        return sorted(list(dict.fromkeys(ports)))
    except Exception:
        paths = []
        paths.extend(Path("/dev").glob("tty.*"))
        paths.extend(Path("/dev").glob("cu.*"))
        return sorted(list(dict.fromkeys([str(p) for p in paths])))


def _has_flash_images(base_dir: Path) -> bool:
    return (
        (base_dir / "bootloader.bin").exists()
        and (base_dir / "partitions.bin").exists()
        and (base_dir / "firmware.bin").exists()
    )


def _repo_root() -> Path:
    # Deterministic for local-dev layout:
    # resources/python-backend/services/firmware.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def resolve_firmware_dir() -> Optional[Path]:
    env_dir = (os.environ.get("ELATO_FIRMWARE_DIR") or "").strip()
    base_dir = Path(env_dir).expanduser().resolve() if env_dir else _repo_root() / "resources" / "firmware"
    if _has_flash_images(base_dir):
        return base_dir
    return None


def prepare_firmware_images() -> tuple[Optional[Path], str]:
    existing = resolve_firmware_dir()
    if existing:
        return existing, f"Using firmware images from: {existing}"
    return None, "Firmware images are missing from bundled resources."


def firmware_bin_path() -> Path:
    resolved = resolve_firmware_dir()
    if resolved:
        return resolved / "firmware.bin"
    env_dir = (os.environ.get("ELATO_FIRMWARE_DIR") or "").strip()
    base_dir = Path(env_dir).expanduser().resolve() if env_dir else _repo_root() / "resources" / "firmware"
    return base_dir / "firmware.bin"


def _resolve_flash_files(firmware_path: Path, offset: str) -> List[Tuple[str, Path]]:
    base_dir = firmware_path.parent
    bootloader = base_dir / "bootloader.bin"
    partitions = base_dir / "partitions.bin"
    firmware = base_dir / "firmware.bin"

    if not (bootloader.exists() and partitions.exists() and firmware.exists()):
        raise FileNotFoundError(
            "Required firmware images missing. Expected bootloader.bin, partitions.bin, and firmware.bin."
        )
    return [
        ("0x0000", bootloader),
        ("0x8000", partitions),
        ("0x10000", firmware),
    ]


def run_firmware_flash(
    *,
    port: str,
    baud: int,
    chip: str,
    offset: str,
    firmware_path: Path,
) -> Dict[str, object]:
    flash_files = _resolve_flash_files(firmware_path, offset)
    cmd = [
        sys.executable,
        "-m",
        "esptool",
        "--before",
        "default-reset",
        "--after",
        "hard-reset",
        "--chip",
        chip,
        "--port",
        port,
        "--baud",
        str(baud),
        "write-flash",
        "-z",
    ]
    for flash_offset, flash_path in flash_files:
        cmd.append(flash_offset)
        cmd.append(str(flash_path))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + ("\n" if proc.stdout and proc.stderr else "") + (proc.stderr or "")
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "command": " ".join(cmd),
        "output": out,
    }
