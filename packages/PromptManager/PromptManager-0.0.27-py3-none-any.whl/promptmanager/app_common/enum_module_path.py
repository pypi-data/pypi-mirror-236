from enum import Enum

from promptmanager.PromptManager.settings.base import BASE_DIR


class ModulePath(Enum):
    PYTHON3_SCRIPT = {'module_id': '00000000-0000-0000-1111-000000000001',
                      'script_path': BASE_DIR / "script/python3_script.py"}

    TEXT_SEGMENTATION = {'module_id': '00000000-0000-0000-bbbb-000000000001',
                         'script_path': BASE_DIR / "script/text_segmentation.py"}

    TEXT_TRUNCATION = {'module_id': '00000000-0000-0000-bbbb-000000000002',
                       'script_path': BASE_DIR / "script/text_truncation.py"}

    CHROMA_WRITER = {'module_id': '00000000-0000-0000-cccc-000000000001',
                     'script_path': BASE_DIR / "script/chroma_writer.py"}

    CHROMA_READER = {'module_id': '00000000-0000-0000-cccc-000000000002',
                     'script_path': BASE_DIR / "script/chroma_reader.py"}

    DINGO_WRITER = {'module_id': '00000000-0000-0000-cccc-000000000003',
                    'script_path': BASE_DIR / "script/dingodb_writer.py"}

    DINGO_READER = {'module_id': '00000000-0000-0000-cccc-000000000004',
                    'script_path': BASE_DIR / "script/dingodb_reader.py"}

    CSV_LOADER = {'module_id': '00000000-0000-0000-eeee-000000000001',
                  'script_path': BASE_DIR / "script/csv_loader.py"}

    TEXT_LOADER = {'module_id': '00000000-0000-0000-eeee-000000000002',
                   'script_path': BASE_DIR / "script/text_loader.py"}

    @staticmethod
    def get_module_path_by_id(module_id: str) -> str:
        for module in ModulePath:
            if module.value['module_id'] == module_id:
                return str(module.value['script_path'])

        from promptmanager.exception import exception
        raise exception.FLOW_MODULE_ID_NOT_SUPPORT
