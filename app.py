import asyncio
import enum
import json
import pydantic
import requests

from typing import Any, Dict, List, Optional


class MovementSpeed(pydantic.BaseModel):
    climb: Optional[int]
    fly: Optional[int]
    swim: Optional[int]
    walk: Optional[int]


class AbilityScores:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Alignment(str, enum.Enum):
    LawfulEvil = "lawful evil"
    LawfulNeutral = "lawful neutral"
    LawfulGood = "lawful good"
    ChaoticEvil = "chaotic evil"
    ChaoticNeutral = "chaotic neutral"
    ChaoticGood = "chaotic good"
    NeutralEvil = "neutral evil"
    TrueNeutral = "true neutral"
    NeutralGood = "neutral good"


class Size(str, enum.Enum):
    Tiny = "Tiny"
    Small = "Small"
    Medium = "Medium"
    Large = "Large"
    Huge = "Huge"
    Gargantuan = "Gargantuan"


class Creature(pydantic.BaseModel):
    name: str
    size: Size
    alignment: Alignment


class Monster(pydantic.BaseModel):
    name: str
    size: str
    type: str
    alignment: Alignment
    armor_class: int
    hit_points: int
    hit_dice: str
    speed: MovementSpeed
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Index(pydantic.BaseModel):
    index: str
    name: str
    url: str


class APIList(pydantic.BaseModel):
    count: int
    results: List[Index]


class DNDAPI:
    def __init__(self) -> None:
        self._base_url: str = "https://www.dnd5eapi.co/api"

    @property
    def base_url(self) -> str:
        return self._base_url

    def _query_api(self, url: str) -> Dict[Any, Any]:
        api_response: str = requests.get(url=f"{self._base_url}/{url}")
        return json.loads(s=api_response.text)

    def monster_list(self) -> APIList:
        return APIList.parse_obj(obj=self._query_api(url="monsters"))

    def spell_list(self) -> APIList:
        """Get List of Spells

        https://www.dnd5eapi.co/docs/#get-/api/spells
        """
        return APIList.parse_obj(obj=self._query_api(url="spells"))

    def monster_details(self, monster: Index) -> Monster:
        monster = self._query_api(url=f"monsters/{monster.index}")
        return monster


async def main() -> None:
    dnd_api: DNDAPI = DNDAPI()
    print("MONSTERS")
    print(dnd_api.monster_list())
    print("SPELLS")
    print(dnd_api.spell_list())


if __name__ == "__main__":
    asyncio.run(main=main())
