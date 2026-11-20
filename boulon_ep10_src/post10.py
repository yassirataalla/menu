# ---- ep10 render quality overrides (after camtail) ----
scene.cycles.samples = int(os.environ.get("SAMPLES", "8")); scene.cycles.max_bounces = 4; scene.cycles.glossy_bounces = 3
scene.cycles.denoising_quality = os.environ.get("DENOQ", "FAST"); cam_d.dof.aperture_blades = 7
