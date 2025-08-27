def print_initial(frame_size):
    initial_display = [" "] * frame_size
    initial_str = "[" + "|".join(f"{str(p):^3}" for p in initial_display) + "]"
    print(f"Initial-> {initial_str}")
    print()


def print_frames(frames, frame_size, page, is_hit):
    display = frames + [" "] * (frame_size - len(frames))
    frames_str = "[" + "|".join(f"{str(p):^3}" for p in display) + "]"
    status = "HIT" if is_hit else "FAULT"
    print(f"PAGE {page} -> {frames_str} ({status})")


def print_optimal_frames(frames, frame_size, page, is_hit, future_info=None):
    display = frames + [" "] * (frame_size - len(frames))
    frames_str = "[" + "|".join(f"{str(p):^3}" for p in display) + "]"
    status = "HIT" if is_hit else "FAULT"

    result = f"PAGE {page} -> {frames_str} ({status})"

    if future_info and not is_hit and len(frames) == frame_size:
        future_str = "  Future: "
        for frame_page in frames:
            if frame_page in future_info:
                if future_info[frame_page] == 999:
                    future_str += f"{frame_page}(Never) "
                else:
                    future_str += f"{frame_page}(Step {future_info[frame_page]+1}) "
        result += "\n" + future_str

    print(result)


def print_lru_frames(frames, frame_size, page, is_hit, ages=None):
    display = frames + [" "] * (frame_size - len(frames))

    if ages:
        frame_parts = []
        for p in display:
            if p == " ":
                frame_parts.append("   ")
            else:
                age = ages.get(p, 0)
                frame_parts.append(f"{p}({age})")
        frames_str = "[" + "|".join(f"{part:^5}" for part in frame_parts) + "]"
    else:
        frames_str = "[" + "|".join(f"{str(p):^3}" for p in display) + "]"

    status = "HIT" if is_hit else "FAULT"
    print(f"PAGE {page} -> {frames_str} ({status})")


def optimal(pages, frame_size):
    print("\n=== OPTIMAL ===")
    print('SEQUENCE:', pages)

    frames = list()
    page_faults = 0
    print_initial(frame_size)

    for i, page in enumerate(pages):
        if page in frames:
            print_optimal_frames(frames, frame_size, page, True)
        else:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
                print_optimal_frames(frames, frame_size, page, False)
            else:
                future = dict()
                for frame_page in frames:
                    try:
                        next_use = pages.index(frame_page, i + 1)
                        future[frame_page] = next_use
                    except ValueError:
                        future[frame_page] = 999

                victim = max(future, key=future.get)
                frames[frames.index(victim)] = page

                print_optimal_frames(frames, frame_size, page, False, future)

    print(f"\nTotal page faults: {page_faults}")
    return page_faults


def lru(pages, frame_size):
    print("\n=== LRU ===")

    frames = list()
    ages = dict()
    page_faults = 0
    print_initial(frame_size)

    for page in pages:
        for p in ages:
            ages[p] += 1

        if page in frames:
            ages[page] = 0
            print_lru_frames(frames, frame_size, page, True, ages)
        else:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
                ages[page] = 0
            else:
                oldest_page = max(ages, key=ages.get)
                oldest_idx = frames.index(oldest_page)

                frames[oldest_idx] = page
                del ages[oldest_page]
                ages[page] = 0

            print_lru_frames(frames, frame_size, page, False, ages)

    print(f"\nTotal page faults: {page_faults}")
    return page_faults


def print_clock(frames, frame_size, page, is_hit, reference_bits, clock_hand):
    display = frames + [" "] * (frame_size - len(frames))

    frame_parts = []
    for i, p in enumerate(display):
        if p == " ":
            frame_parts.append("   ")
        else:
            ref_bit = reference_bits.get(p, 0)
            pointer = "←" if i == clock_hand and len(
                frames) == frame_size else " "
            frame_parts.append(f"{p}({ref_bit}){pointer}")

    frames_str = "[" + "|".join(f"{part:^6}" for part in frame_parts) + "]"
    status = "HIT" if is_hit else "FAULT"
    print(f"PAGE {page} -> {frames_str} ({status})")


def clock(pages, frame_size):
    print("\n=== CLOCK ===")
    frames = list()
    reference_bits = dict()
    clock_hand = 0
    page_faults = 0

    print_initial(frame_size)

    for page in pages:
        if page in frames:
            reference_bits[page] = 1
            print_clock(frames, frame_size, page, True,
                        reference_bits, clock_hand)
        else:
            page_faults += 1

            if len(frames) < frame_size:
                frames.append(page)
                reference_bits[page] = 1
            else:
                while True:
                    current_page = frames[clock_hand]
                    if reference_bits[current_page] == 0:
                        frames[clock_hand] = page
                        reference_bits[page] = 1
                        if current_page in reference_bits:
                            del reference_bits[current_page]
                        clock_hand = (clock_hand + 1) % frame_size
                        break
                    else:
                        reference_bits[current_page] = 0
                        clock_hand = (clock_hand + 1) % frame_size

            print_clock(frames, frame_size, page, False,
                        reference_bits, clock_hand)

    print(f"\nTotal page faults: {page_faults}")
    return page_faults


def fifo(pages, frame_size):
    print("\n=== FIFO ===")
    frames = list()
    page_faults = 0

    print_initial(frame_size)

    for page in pages:
        if page in frames:
            print_frames(frames, frame_size, page, True)
        else:
            page_faults += 1

            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            print_frames(frames, frame_size, page, False)

    print(f"\nTotal page faults: {page_faults}")
    return page_faults


if __name__ == "__main__":
    page_sequence = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    frame_size = 3

    print("PAGE REPLACEMENT ALGORITHM COMPARISON")
    print("="*50)

    fifo_faults = fifo(page_sequence, frame_size)
    clock_faults = clock(page_sequence, frame_size)
    optimal_faults = optimal(page_sequence, frame_size)
    lru_faults = lru(page_sequence, frame_size)

    print("\n" + "="*50)
    print(f"FIFO:    {fifo_faults} page faults")
    print(f"CLOCK:   {clock_faults} page faults")
    print(f"OPTIMAL: {optimal_faults} page faults")
    print(f"LRU:     {lru_faults} page faults")
