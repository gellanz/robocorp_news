from robocorp.tasks import task
from robocorp import workitems
from robocorp.workitems import Input
from robocorp import browser
from news_robot import Robot


@task
def robot_spare_bin_python():
    for item in workitems.inputs:
        robot = Robot(
            browser=browser,
            phrase=item.payload["phrase"],
            type_news=item.payload["type_news"],
            sort_by=item.payload["sort_by"],
        )
        news_locator = robot.navigate()
        news_list = robot.process_ul_element(news_locator)
        robot.export_to_excel(news_list, f'./output/news_{item.payload["phrase"]}.xlsx')
