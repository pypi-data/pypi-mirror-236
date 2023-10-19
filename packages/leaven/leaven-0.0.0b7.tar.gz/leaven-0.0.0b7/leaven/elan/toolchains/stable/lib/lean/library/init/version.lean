prelude
import init.data.nat.basic init.data.string.basic

def lean.version : nat × nat × nat :=
(3, 48, 0)

def lean.githash : string :=
"283f6ed8083ab4dd7c36300f31816c5cb793f2f7"

def lean.is_release : bool :=
1 ≠ 0

/-- Additional version description like "nightly-2018-03-11" -/
def lean.special_version_desc : string :=
""
