import os
from datetime import datetime

import psutil
from mcp.server.mcpserver import MCPServer


mcp = MCPServer("SystemAndFileManager")


# 1. TOOL: Sistem kaynaklarını göster
@mcp.tool()
def get_system_stats() -> dict:
    """Bilgisayarın anlık CPU, RAM ve Disk kullanımını döndürür."""

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": {
            "usage_percent": cpu_usage,
            "core_count": psutil.cpu_count(logical=True),
        },
        "ram": {
            "total_gb": round(ram.total / (1024**3), 2),
            "used_gb": round(ram.used / (1024**3), 2),
            "percent": ram.percent,
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        },
    }


# 2. TOOL: Dosyaya rapor yaz
@mcp.tool()
def write_report(filename: str, content: str) -> str:
    """Rapor veya log dosyasını kaydeder."""

    safe_filename = os.path.basename(filename)

    output_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, safe_filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Dosya başarıyla kaydedildi: {file_path}"


# 3. RESOURCE: Canlı sistem durumu
@mcp.resource("system://live-status")
def get_live_status() -> str:
    """Bilgisayarın genel durumunu gösteren canlı kaynak."""

    boot_time = datetime.fromtimestamp(
        psutil.boot_time()
    ).strftime("%Y-%m-%d %H:%M:%S")

    running_processes_count = len(psutil.pids())

    return (
        "=== SİSTEM DURUM RAPORU ===\n"
        f"Son Açılış Zamanı: {boot_time}\n"
        f"Aktif Süreç Sayısı: {running_processes_count}\n"
        "Durum: Sağlıklı\n"
        f"Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


if __name__ == "__main__":
    mcp.run()