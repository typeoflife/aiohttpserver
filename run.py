import bcrypt
from aiohttp import web
from models import db, PG_DATABASE\
    , UserModel, AdvModel
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

app = web.Application()


async def init_orm(app):
    await db.set_bind(PG_DATABASE)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


class UserValidationModel(BaseModel):
    username: str
    email: str
    password: str


class AdvValidationModel(BaseModel):
    title: str
    text: str
    user_id: int


class UserView(web.View):

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await UserModel.get(user_id)
        if not user:
            return web.json_response({
                'status': 'error',
                'message': 'user not found'
            }, status=404)
        user_data = user.to_dict()
        user_data.pop('password')
        return web.json_response(user_data)

    async def post(self):
        user_date = await self.request.json()
        try:
            user_data_validated = UserValidationModel(**user_date).dict()
        except ValidationError as error:
            return web.json_response({
                'status': 'error',
                'message': error.errors()
            })
        user_data_validated['password'] = bcrypt.hashpw(user_data_validated['password'].encode(),
                                                        bcrypt.gensalt()).decode()
        try:
            new_user = await UserModel.create(**user_data_validated)
        except UniqueViolationError as error:
            return web.json_response({
                'status': 'error',
                'message': error.detail
            }, status=409)
        response_data = new_user.to_dict()
        response_data.pop('password')
        return web.json_response(
            response_data
        )


class AdvView(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await AdvModel.get(adv_id)
        if not adv:
            return web.json_response({
                'status': 'error',
                'message': 'adv not found'
            }, status=404)
        adv_data = adv.to_dict()
        adv_data.pop('date')
        return web.json_response(adv_data)

    async def post(self):
        adv_date = await self.request.json()
        try:
            user_data_validated = AdvValidationModel(**adv_date).dict()
        except ValidationError as error:
            return web.json_response({
                'status': 'error',
                'message': error.errors()
            })
        try:
            new_adv = await AdvModel.create(**user_data_validated)
        except ForeignKeyViolationError as error:
            return web.json_response({
                'status': 'error',
                'message': error.detail
            }, status=409)
        print(new_adv.to_dict()['date'])
        return web.json_response({
            'status': 'Adv create',
            'title': new_adv.to_dict()['title'],
            'text': new_adv.to_dict()['text']
        })



if __name__ == '__main__':
    app.add_routes([web.get('/user/{user_id:\d+}', UserView)])
    app.add_routes([web.post('/user', UserView)])
    app.add_routes([web.get('/adv/{adv_id:\d+}', AdvView)])
    app.add_routes([web.post('/adv', AdvView)])
    app.cleanup_ctx.append(init_orm)
    web.run_app(app, host='0.0.0.0', port=8080)
