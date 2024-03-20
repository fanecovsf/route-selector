from app.link import Link
from datetime import timedelta


class Route:
    """
    Object to handle routes informations
    """

    time_to_arrive: str
    km: float
    points: list[str]

    def __init__(self, time_to_arrive: str, km: float, points: list[str]) -> None:
        self.time_to_arrive = time_to_arrive
        self.km = km
        self.points = points
        pass

    def __str__(self) -> str:
        return f'''Route: {" > ".join(point for point in self.points)}
        Km: {self.km}
        Time to arrive: {self.time_to_arrive}
        '''
    
    @property
    def duration(self) -> timedelta | None:
        """
        Method to calculate the trip duration using timedelta
        """

        if 'h' in self.time_to_arrive and 'min' in self.time_to_arrive:
            hours = int(self.time_to_arrive.split(' h')[0])
            minutes = int(self.time_to_arrive.split(' ')[2])
            return timedelta(hours=hours, minutes=minutes)
        
        if 'h' in self.time_to_arrive:
            hours = int(self.time_to_arrive.split(' ')[0])
            return timedelta(hours=hours)
        
        if 'min' in self.time_to_arrive:
            minutes = int(self.time_to_arrive.split(' ')[0])
            return timedelta(minutes=minutes)
        
        return None



def make_possibilities(array: list[str]) -> list[list]:
    # This function will calculate all of the route possibilities and return an array with the possibilities

    if len(array) == 1:
        return [array]

    all_possibilities = []

    for i in range(len(array)):
        first_element = array[i]
        rem_elements = array[:i] + array[i+1:]

        for poss in make_possibilities(rem_elements):
            all_possibilities.append([first_element] + poss)

    return all_possibilities


def make_routes(link: Link, destinations: list[str]) -> list[Route]:
    # This function will make all the routes possibilities to see wich one is the better

    first_route = True
    route_list = []

    for route in make_possibilities(destinations):
        
        link.clear_field('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input')
        link.send_keys('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input', route[0])
        link.press_key('enter')

        link.clear_field('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input')
        link.send_keys('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input', route[1])
        link.press_key('enter')

        if len(route) > 2:
            div_number = 3

            if first_route:
                for _ in range(len(route) - 2):
                    link.click_element('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/button')
                    link.clear_field(f'/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[{div_number}]/div[2]/div[1]/div/input')
                    link.send_keys(f'/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[{div_number}]/div[2]/div[1]/div/input', route[div_number-1])
                    link.press_key('enter')

                    div_number += 1

                first_route = False

            else:
                for _ in range(len(route) - 2):
                    link.clear_field(f'/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[{div_number}]/div[2]/div[1]/div/input')
                    link.send_keys(f'/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[{div_number}]/div[2]/div[1]/div/input', route[div_number-1])
                    link.press_key('enter')

                    div_number += 1

        route_list.append(Route(
            time_to_arrive=link.element_text('//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[1]').strip(),
            km=float(link.element_text('//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div').split(' ')[0].replace(',', '.').strip()),
            points=route
        ))

    return route_list


def main(destinations: list[str]) -> bool:
    if len(destinations) < 2:
        return False
    
    # Link instance

    link = Link(
        url='https://www.google.com.br/maps',
        sleep=2
    )

    link.open()
    link.maximize()

    link.click_element('//*[@id="hArJGc"]')

    link.click_element('//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[2]/button')
    
    routes = make_routes(link, destinations)

    link.quit()

    duration_sorted_routes = sorted(routes, key=lambda x: x.duration)
    km_sorted_routes = sorted(routes, key=lambda x: x.km)

    print(f'Viagem com menor duração: {duration_sorted_routes[0]}\n')
    print(f'Viagem com menor quilometragem: {km_sorted_routes[0]}\n')



main(['Hortolândia', 'Campinas', 'Sumaré'])

