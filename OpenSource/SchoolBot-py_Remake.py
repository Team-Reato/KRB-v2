import discord
import neispy
import discord.ext
from discord.ext import commands
import datetime

token="Njg1NzE1Mzg2NzQ1ODgwNTgx.XtXxQA.CCapnJOI80brzyf-BEi7i8_8DEE"
neistoken="2f847a87e1e6496ba600bf3811316737"
bot = commands.Bot(command_prefix="]")
n = datetime.datetime.now()
NOW = f'{n.year}{n.month}{n.day}'
neis = neispy.AsyncClient(neistoken)

@bot.event
async def on_ready():
    print("I'm Ready!")

@bot.event
async def on_message(message):
    if message.content.startswith("카린아 학교 정보"):
        if message.content.endswith("학교"):
            school = message.content[10:]
            info = await neis.schoolInfo(SCHUL_NM=school)
        else:
            school = message.content[10:12]
            info = await neis.schoolInfo(ATPT_OFCDC_SC_CODE=school)
        try:
            embed = discord.Embed(title=f'{info.SCHUL_NM}의 정보입니다.',description=info.ENG_SCHUL_NM)
            embed.add_field(name="시도교육청코드", value=info.ATPT_OFCDC_SC_CODE)
            embed.add_field(name="시도교육청명", value=info.ATPT_OFCDC_SC_NM)
            embed.add_field(name="표준학교코드", value=info.SD_SCHUL_CODE)
            embed.add_field(name="학교종류명", value=info.SCHUL_KND_SC_NM)
            embed.add_field(name="소재지명", value=info.LCTN_SC_NM)
            embed.add_field(name="관할조직명",value=info.JU_ORG_NM)
            embed.add_field(name="설립명", value=info.FOND_SC_NM)
            embed.add_field(name="도로명 우편주소", value=info.ORG_RDNZC)
            embed.add_field(name="도로명주소", value=info.ORG_RDNMA)
            embed.add_field(name="도로명 상세주소", value=info.ORG_RDNDA)
            embed.add_field(name="전화번호", value=info.ORG_TELNO)
            embed.add_field(name="홈페이지", value=f"[링크]({info.HMPG_ADRES})")
            embed.add_field(name="남녀공학구분명", value=info.COEDU_SC_NM)
            embed.add_field(name="팩스", value=info.ORG_FAXNO)
            embed.add_field(name="고등학교 구분명", value=info.HS_SC_NM)
            embed.add_field(name="산업체특별학급존재여부", value=info.INDST_SPECL_CCCCL_EXST_YN)
            embed.add_field(name="고등학교일반실업구분명", value=info.HS_GNRL_BUSNS_SC_NM)
            embed.add_field(name="특수목적고등학교계열명", value=info.SPCLY_PURPS_HS_ORD_NM)
            embed.add_field(name="입시전후기구분명", value=info.ENE_BFE_SEHF_SC_NM)
            embed.add_field(name="주야구분명", value=info.DGHT_SC_NM)
            embed.add_field(name="설립일자", value=info.FOND_YMD)
            embed.add_field(name="개교기념일", value=info.FOAS_MEMRD)
            embed.add_field(name="적재일시", value=info.LOAD_DTM)
            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send("오류 발생! 재시도 해주세요.")
    if message.content.startswith("카린아 학교 급식"):
        if message.content[19:] is None:
            await message.channel.send("어머나, 정보가 검색되지 않아요! `카린아 학교 급식 날짜 학교명` 대로 입력해주세요!")
        else:
            school = message.content[18:]
            nalja = message.content[10:17]
            info = await neis.schoolInfo(SCHUL_NM=school)
            AE = info.ATPT_OFCDC_SC_CODE
            SE = info.SD_SCHUL_CODE
            scmeal = await neis.mealServiceDietInfo(AE, SE, MLSV_YMD=nalja)
            meal = scmeal.DDISH_NM.replace('<br/>', '\n')
            embed = discord.Embed(title=f"{info.SCHUL_NM}의 급식입니다.", description=meal)
            embed.add_field(name=f"{message.author} | {NOW}", value=meal.meal())
            await message.channel.send(embed=embed)

bot.run(token)