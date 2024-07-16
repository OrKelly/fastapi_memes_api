from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.media_storage.minio import MinioStorage
from app.memes.dao import MemeDAO
from app.memes.exceptions import MemeNotFound, NotMemeAuthorException
from app.memes.pagination import get_pagination_params, paginate
from app.memes.schemas import SMemes
from app.memes.utils import verify_is_meme_author
from app.users.auth import get_current_user

router = APIRouter(
    prefix='/memes',
    tags=['Memes'],
)


@router.get('')
async def get_all_memes(pagination_params=Depends(get_pagination_params)):
    memes = await MemeDAO.find_all()
    if not memes:
        return {'response': 'К сожалению, никто еще не сделал мемов :('}
    return paginate(pagination_params, memes, SMemes)


@router.get('/{meme_id}')
async def get_specified_meme(meme_id: int) -> SMemes:
    meme = await MemeDAO.find_one_or_none(id=meme_id)
    if not meme:
        raise MemeNotFound
    return meme


@router.post('/create_meme')
async def create_meme(image: UploadFile = File(...),
                      desc: str = Query(None, description='Описание мема'),
                      user=Depends(get_current_user)):
    url = MinioStorage().upload_image(image)
    await MemeDAO.add(url=url, desc=desc, author=user.id)
    return {'response': 'Ваш мем был добавлен!'}


@router.put('/update_meme/{meme_id}')
async def updated_meme(meme_id: int,
                       image: UploadFile = File(None),
                       desc: str = Query(None, description='Описание мема'),
                       user=Depends(get_current_user)):
    await verify_is_meme_author(user, meme_id)
    updated_data = {'desc': desc, 'url': ''}
    if image:
        url = MinioStorage().upload_image(image)
        updated_data['url'] = url
    await MemeDAO.update(instance_id=meme_id,
                         desc=updated_data['desc'],
                         url=updated_data['url'])

    return {'response': 'Ваш мем был обновлен!'}


@router.delete('/delete_meme/{meme_id}')
async def delete_meme(meme_id: int,
                      user=Depends(get_current_user)):
    await verify_is_meme_author(user, meme_id)
    await MemeDAO.delete(instance_id=meme_id)
    return {'response': 'Мем был удален!'}
