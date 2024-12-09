# filename = 'test'
filename = 'input'

data = list(map(int, open(filename, 'r').read().strip()))
file_sectors = list(enumerate(data[::2]))
empty_sectors = data[1::2]

free_chunk = 0
defragged = []
file_id, sectors_remaining = file_sectors.pop()
while file_sectors:
    if free_chunk < sectors_remaining:
        if free_chunk:
            defragged.append((file_id, free_chunk))
            sectors_remaining -= free_chunk
        free_chunk = empty_sectors.pop(0)
        defragged.append(file_sectors.pop(0))

    while sectors_remaining <= free_chunk:
        if sectors_remaining:
            defragged.append((file_id, sectors_remaining))
            free_chunk -= sectors_remaining
        file_id, sectors_remaining = file_sectors.pop()

if free_chunk:
    defragged.append((file_id, sectors_remaining))

# print(data)
# print(defragged)
# for f_id, sectors in defragged:
#     print(str(f_id) * sectors, end='')
# print()
checksum = sum(i*n for i, n in enumerate(sum(([k]*v for k, v in defragged), [])))
print(checksum)
