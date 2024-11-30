import json, os
from threading import Thread, Lock
from json_parsers.jparser import jparser_multi, jparser

if __name__ == '__main__':
    lock = Lock()
    # testing multi bill json input
    here = os.path.dirname(os.path.abspath(__file__))
    json_input = here + '\\json_parsers\\' + 'test.json'

    with open(json_input) as file:
        parsed_input = json.load(file)

    # input the multi-bill json
    # this will currently "fail" due to it existing in the db already
    # delete local.db in the API dir and rerun to see a successful write
    jpm_thread = Thread(target=jparser_multi(parsed_input), args=(lock))
    jpm_thread.start()
    # not sure if these join statements are needed, as it performs the same when they are commented out,
    # but because they cause the program to wait until the thread finishes, i'll keep them there for good measure
    jpm_thread.join()

    # testing single bill json input
    jsingle_input = here + '\\json_parsers\\' + 'test_single.json'

    with open(jsingle_input) as file:
        parsed_input = json.load(file)

    # threading is necessary to prevent race conditions
    # as we are currently perform multiple write operations to a single database
    jp_thread = Thread(target=jparser(parsed_input), args=(lock))
    jp_thread.start()
    jp_thread.join()
