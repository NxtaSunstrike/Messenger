from typing import Dict


from Db.Postgres.Crud.Repositories import UserRepository

class UserService:

    def __init__(self, UserRepo: UserRepository) -> None:
        self.UserRepo: UserRepository = UserRepo


    async def GetUser(self, UUID: str)->Dict:
        User = await self.UserRepo.GetUser(UUID = UUID)
        return User
    

    async def CreateUser(self, User: Dict)->Dict:
        User = await self.UserRepo.CreateUser(User = User)
        return User
    

    async def DeleteUser(self, UUID: str)->Dict:
        User = await self.UserRepo.DeleteUser(UUID = UUID)
        return User
    

    async def CheckUser(self, email: str)->Dict:
        User = await self.UserRepo.CheckUser(email = email)
        return User


    async def AddIp(self, UUID: str, Ip: str)->Dict:
        User = await self.UserRepo.AddIp(UUID = UUID, Ip = Ip)
        return User