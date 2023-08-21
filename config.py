import os
from pathlib import Path

COMPANIES_ID = {"Квантбокс": 2136982,
                "АВСофт": 2355830,
                "Северсталь": 6041,
                "HYPERPC": 1199534,
                "ЛАНИТ": 733,
                "ТЕНЗОР": 1266214,
                "VK": 15478,
                "АйТеко": 115,
                "МДО": 736233,
                "getmatch": 864086,
                "ИнфоТеКС": 3778,
                "Волкрафт": 896866,
                "БПР": 4675140,
                "Ренессанс": 5923,
                "ГИТ": 1066119,
                "IBS": 139,
                "CodeInside": 1096944,
                }

QUERIES_PATH = Path(__file__).resolve().parent / 'database/queries.sql'
DB_CONNECTION_STRING = f"postgresql://postgres:{os.getenv('pgAdmin')}@localhost:5432/hh_parser"
