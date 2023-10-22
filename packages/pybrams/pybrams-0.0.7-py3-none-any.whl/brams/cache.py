import os
import shutil
import glob
from typing import Any, List, Literal, Optional

class Cache:

    root = os.path.join(".", ".cache")
    use_cache = False

    @classmethod
    def remove(cls, filepath: str) -> None:

        try:
        
            os.remove(filepath)

        except Exception:

            pass

    @classmethod
    def clear(cls, metadata_only: bool = False, systems: Optional[List[str]] = None) -> None:

        if metadata_only:

            for file in glob.glob(os.path.join(cls.root, "??????.json")):

                cls.remove(file)

            for file in glob.glob(os.path.join(cls.root, "??????_SYS???.json")):

                cls.remove(file)

        
        elif systems:

            for system in systems: 

                for file in glob.glob(os.path.join(cls.root, f"{system}*json")):
                    
                    cls.remove(file)

                for file in glob.glob(os.path.join(cls.root, f"*{system}*wav")):
                    
                    cls.remove(file)     
                
        else:

            shutil.rmtree(cls.root, ignore_errors=True)

    @classmethod
    def cache(cls, key: str, data: Any, json: bool = True) -> None:

        if cls.use_cache:

            if not os.path.exists(cls.root):

                os.mkdir(cls.root)

            print(f"[C] <== {key}")

            path = f"{key}.json" if json else key
            mode = "w" if json else "wb"

            with open(os.path.join(cls.root, path), mode) as file:

                file.write(data)


    @classmethod
    def get(cls, key: str, json: bool = True) -> Any | Literal[False]:

        if cls.use_cache:

            path = f"{key}.json" if json else key
            mode = "r" if json else "rb"

            if not os.path.exists(os.path.join(cls.root, path)):

                return False

            print(f"[C] ==> {key}")

            with open(os.path.join(cls.root, path), mode) as file:

                return file.read()

        return False

