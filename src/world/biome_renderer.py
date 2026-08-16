# biome_renderer.py 
# Used ursina to render the world grid as 3D cubes
# Test only - Might be removed later if different rendering method is preferred


from ursina import Entity, color, Vec3
from src.core.constants import TILE_SIZE, HEIGHT_SCALE, WATER_RENDER_HEIGHT, BIOME_COLORS


_tile_entities = {}


def build_terrain(world):
	global _tile_entities
	clear_terrain()

	offset_x = -world.width * TILE_SIZE / 2
	offset_z = -world.height * TILE_SIZE / 2

	for cell in world.get_all_cells():
		_create_tile_entity(cell, offset_x, offset_z)


def _create_tile_entity(cell, offset_x, offset_z):
	"""create a single tile entity for a cell."""
	global _tile_entities

	if cell.biome == "water":
		render_height = WATER_RENDER_HEIGHT * HEIGHT_SCALE
	else:
		render_height = cell.height * HEIGHT_SCALE

	r, g, b = BIOME_COLORS.get(cell.biome, (0.5, 0.5, 0.5))

	
	e = Entity(
		model="cube",
		color=color.rgb(int(r * 255), int(g * 255), int(b * 255)),
		position=Vec3(
			cell.x * TILE_SIZE + offset_x,
			render_height / 2,      
			cell.y * TILE_SIZE + offset_z,
		),
		scale=Vec3(TILE_SIZE, max(render_height, 0.1), TILE_SIZE),
		collider="box",            
	)
	e.grid_x = cell.x
	e.grid_y = cell.y

	cell.entity = e
	_tile_entities[(cell.x, cell.y)] = e


def update_cell_visual(cell):
	e = _tile_entities.get((cell.x, cell.y))
	if e is None:
		return

	if cell.biome == "water":
		render_height = WATER_RENDER_HEIGHT * HEIGHT_SCALE
	else:
		render_height = cell.height * HEIGHT_SCALE

	r, g, b = BIOME_COLORS.get(cell.biome, (0.5, 0.5, 0.5))
	e.color = color.rgb(int(r * 255), int(g * 255), int(b * 255))
	e.y = render_height / 2
	e.scale_y = max(render_height, 0.1)


def clear_terrain():
	global _tile_entities
	for e in _tile_entities.values():
		if e:
			e.disable()
	_tile_entities.clear()