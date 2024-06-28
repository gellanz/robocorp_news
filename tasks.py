from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
from robocorp import browser
from news_robot import Robot


@task
def robot_spare_bin_python():
    robot = Robot(browser=browser, phrase="Biden")
    news_locator = robot.navigate()
    news_list = robot.process_ul_element(news_locator)
    robot.export_to_excel(news_list, "./output/news.xlsx")


def process_robocloud_workitem():
    customers = [{"id": 1, "name": "Apple"}, {"id": 2, "name": "Microsoft"}]
    wi = WorkItems()
    wi.get_input_work_item()
    wi.set_work_item_variable("customers", customers)
