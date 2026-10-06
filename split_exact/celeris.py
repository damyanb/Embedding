from dataclasses import dataclass, field, asdict
from typing import List, Dict


@dataclass
class Constants:
    # Computational domain dimensions
    WIDTH: int = field(
        default=800, metadata={"description": "Width of the computational domain."}
    )
    HEIGHT: int = field(
        default=600, metadata={"description": "Height of the computational domain."}
    )

    # Grid cell dimensions
    dx: float = field(
        default=1.0, metadata={"description": "Cell size in the x direction."}
    )
    dy: float = field(
        default=1.0, metadata={"description": "Cell size in the y direction."}
    )

    # Time-stepping parameters
    Courant_num: float = field(
        default=0.15,
        metadata={
            "description": "Target Courant number. ~0.25 for P-C, ~0.05 for explicit methods."
        },
    )
    timeScheme: int = field(
        default=2,
        metadata={
            "description": "Time integration choices: 0: Euler, 1: 3rd-order A-B predictor, 2: A-B 4th-order predictor+corrector."
        },
    )
    pred_or_corrector: int = field(
        default=1,
        metadata={
            "description": "Variable which tells render loop which stage solver is in."
        },
    )

    # Wave model parameters
    NLSW_or_Bous: int = field(
        default=0,
        metadata={
            "description": "Choose 0 for Non-linear Shallow Water (NLSW) or 1 for Boussinesq."
        },
    )
    Bcoef: float = field(
        default=1.0 / 15.0,
        metadata={
            "description": "Dispersion parameter, 1/15 is optimum value for this set of equations."
        },
    )

    # Physical parameters
    g: float = field(
        default=9.80665, metadata={"description": "Gravitational constant."}
    )
    seaLevel: float = field(
        default=0.0,
        metadata={
            "description": "Water level shift from given datum - deprecated - no longer used."
        },
    )
    base_depth: float = field(
        default=20.0,
        metadata={
            "description": "Characteristic depth (m), used to estimate time step, use depth in area of wave generation or expected largest depth in domain."
        },
    )
    Theta: float = field(
        default=2.0,
        metadata={
            "description": "Midmod limiter parameter. 1.0 most dissipative (upwind) to 2.0 least dissipative (centered)."
        },
    )
    friction: float = field(
        default=0.000,
        metadata={
            "description": "Dimensionless friction coefficient, or Manning's 'n', depending on isManning choice."
        },
    )
    isManning: int = field(
        default=0,
        metadata={
            "description": "A boolean friction model value. If 1, 'friction' is Manning's n; otherwise, it is a dimensionless friction factor (Moody)."
        },
    )

    # Breaking model parameters
    useBreakingModel: int = field(
        default=1, metadata={"description": "Include breaking model when == 1."}
    )
    delta_breaking: float = field(
        default=2.0, metadata={"description": "Eddy viscosity coefficient."}
    )
    T_star_coef: float = field(
        default=5.0,
        metadata={
            "description": "Defines length of time until breaking becomes fully developed."
        },
    )
    dzdt_I_coef: float = field(
        default=0.50, metadata={"description": "Start breaking parameter."}
    )
    dzdt_F_coef: float = field(
        default=0.15, metadata={"description": "End breaking parameter."}
    )

    # Boundary condition parameters
    west_boundary_type: int = field(
        default=0,
        metadata={
            "description": "Type of boundary condition at the west boundary. 0: solid wall, 1: sponge layer, 2: waves loaded from file."
        },
    )
    east_boundary_type: int = field(
        default=0,
        metadata={
            "description": "Type of boundary condition at the east boundary. 0: solid wall, 1: sponge layer, 2: waves loaded from file."
        },
    )
    south_boundary_type: int = field(
        default=0,
        metadata={
            "description": "Type of boundary condition at the south boundary. 0: solid wall, 1: sponge layer, 2: waves loaded from file."
        },
    )
    north_boundary_type: int = field(
        default=0,
        metadata={
            "description": "Type of boundary condition at the north boundary. 0: solid wall, 1: sponge layer, 2: waves loaded from file."
        },
    )
    BoundaryWidth: int = field(
        default=20, metadata={"description": "Number of grid points for sponge layer."}
    )
    incident_wave_type: int = field(
        default=-1,
        metadata={
            "description": "0: Sine Wave; 1: TMA Spectrum; 2: Transient Pulse; 3: Solitary Wave; -1: Custom Spectrum."
        },
    )

    # Generic wave parameters used for debug
    amplitude: float = field(
        default=0.0, metadata={"description": "Amplitude of the wave."}
    )
    period: float = field(default=10.0, metadata={"description": "Period of the wave."})
    direction: float = field(
        default=0.0, metadata={"description": "Direction of the wave."}
    )
    rand_phase: float = field(
        default=0.0, metadata={"description": "Random phase of the wave."}
    )

    # Incident wave properties
    incident_wave_H: float = field(
        default=0.0, metadata={"description": "Height of the incident wave (m)."}
    )
    incident_wave_T: float = field(
        default=0.0, metadata={"description": "Period of the incident wave (s)."}
    )
    incident_wave_direction: float = field(
        default=0.0,
        metadata={"description": "Direction of the incident wave (deg CCW from E)."},
    )
    numberOfWaves: int = field(
        default=0, metadata={"description": "Number of wave components to be created."}
    )

    # Vessel motion parameters
    ship_posx: float = field(
        default=-100.0, metadata={"description": "Initial x-position of the ship."}
    )
    ship_posy: float = field(
        default=450.0, metadata={"description": "Initial y-position of the ship."}
    )
    ship_width: float = field(
        default=10.0, metadata={"description": "Beam width of the ship (m)."}
    )
    ship_length: float = field(
        default=30.0, metadata={"description": "Length of the ship (m)."}
    )
    ship_draft: float = field(
        default=2.0, metadata={"description": "Maximum draft of the ship (m)."}
    )
    ship_heading: float = field(
        default=0.0,
        metadata={"description": "Heading of the ship (0 = moving to the east)."},
    )

    # Sediment transport parameters
    useSedTransModel: int = field(
        default=0,
        metadata={"description": "Sediment transport model on/off flag (0 or 1)."},
    )
    sedC1_d50: float = field(
        default=0.2,
        metadata={
            "description": "Median sediment grain size (D50) for Class 1 sediment."
        },
    )
    sedC1_n: float = field(
        default=0.40, metadata={"description": "Porosity for Class 1 sediment."}
    )
    sedC1_psi: float = field(
        default=0.00005, metadata={"description": "Psi value for Class 1 sediment."}
    )
    sedC1_criticalshields: float = field(
        default=0.045,
        metadata={"description": "Critical shields value for Class 1 sediment."},
    )
    sedC1_denrat: float = field(
        default=2.65,
        metadata={
            "description": "Density ratio of sediment to water for Class 1 sediment."
        },
    )

    # Example run
    run_example: int = field(
        default=0,
        metadata={
            "description": "Index corresponding to examples to run. set to -1 for no example"
        },
    )
    exampleDirs: List[str] = field(
        default_factory=lambda: [
            "./examples/Ventura/",
            "./examples/Santa_Cruz/",
            # Add more directories as needed
        ],
        metadata={"description": "Directories for example configurations."},
    )

    # Save data parameters
    create_animation: int = field(
        default=0, metadata={"description": "Flag to create animated GIF (0 or 1)."}
    )
    AnimGif_dt: float = field(
        default=0.25,
        metadata={"description": "Time interval between animated GIF frames."},
    )
    JPEGstack_dt: float = field(
        default=1.0, metadata={"description": "Time between images in JPEG stack."}
    )
    JPEGstack_frames: int = field(
        default=10,
        metadata={"description": "Total number of frames to save in JPEG stack."},
    )

    # Add other fields similarly...
    # Add disturbance parameters
    add_Disturbance: int = field(
        default=-1,
        metadata={"description": "Flag to add disturbance (1 when user clicks 'Add')."},
    )
    disturbanceType: int = field(
        default=1,
        metadata={"description": "Type of disturbance (e.g., 1 = solitary wave)."},
    )
    disturbanceXpos: float = field(
        default=0.0, metadata={"description": "X position of the disturbance."}
    )
    disturbanceYpos: float = field(
        default=0.0, metadata={"description": "Y position of the disturbance."}
    )
    disturbanceCrestamp: float = field(
        default=0.0,
        metadata={"description": "Amplitude of the crest of the disturbance."},
    )
    disturbanceDir: float = field(
        default=0.0, metadata={"description": "Direction of the disturbance."}
    )
    disturbanceWidth: float = field(
        default=0.0, metadata={"description": "Width of the disturbance."}
    )
    disturbanceLength: float = field(
        default=0.0, metadata={"description": "Length of the disturbance."}
    )
    disturbanceDip: float = field(
        default=0.0, metadata={"description": "Dip of the disturbance."}
    )
    disturbanceRake: float = field(
        default=0.0, metadata={"description": "Rake of the disturbance."}
    )

    # Plotting parameters
    colorVal_max: float = field(
        default=1.0,
        metadata={"description": "Maximum value mapped to the highest color."},
    )
    colorVal_min: float = field(
        default=-1.0,
        metadata={"description": "Minimum value mapped to the lowest color."},
    )
    colorMap_choice: int = field(
        default=0,
        metadata={
            "description": "Decision variable for colormap choice during rendering."
        },
    )
    surfaceToPlot: int = field(
        default=0, metadata={"description": "Which surface (eta, u, v, vort) to plot."}
    )
    showBreaking: int = field(
        default=0,
        metadata={"description": "Flag to show breaking (foam) areas (1 = show)."},
    )
    dissipation_threshold: float = field(
        default=0.2, metadata={"description": "Wave slope threshold for breaking."}
    )
    whiteWaterDecayRate: float = field(
        default=0.02, metadata={"description": "Turbulence decay rate."}
    )
    whiteWaterDispersion: float = field(
        default=0.1, metadata={"description": "Turbulence dispersion rate."}
    )
    infiltrationRate: float = field(
        default=0.001, metadata={"description": "Dry beach infiltration rate."}
    )
    ShowLogos: int = field(
        default=1,
        metadata={"description": "Flag to show USC and ERDC logos (1 = show)."},
    )
    GoogleMapOverlay: int = field(
        default=0,
        metadata={"description": "Flag to load satellite image overlay (1 = load)."},
    )
    IsOverlayMapLoaded: int = field(
        default=0,
        metadata={
            "description": "Flag to indicate if overlay map is loaded (1 = loaded)."
        },
    )
    IsGMMapLoaded: int = field(
        default=0,
        metadata={
            "description": "Flag to indicate if Google Map image is loaded (1 = loaded)."
        },
    )
    IsSatMapLoaded: int = field(
        default=0,
        metadata={
            "description": "Flag to indicate if satellite map is loaded (1 = loaded)."
        },
    )
    OverlayUpdate: int = field(
        default=0,
        metadata={"description": "Flag to trigger overlay update (1 = update)."},
    )
    GMapImageWidth: int = field(
        default=512,
        metadata={"description": "Width of the Google Maps image in pixels."},
    )
    GMapImageHeight: int = field(
        default=512,
        metadata={"description": "Height of the Google Maps image in pixels."},
    )
    GMscaleX: float = field(
        default=1.0,
        metadata={
            "description": "Scaling factor in x-direction for Google Maps image."
        },
    )
    GMscaleY: float = field(
        default=1.0,
        metadata={
            "description": "Scaling factor in y-direction for Google Maps image."
        },
    )
    GMoffsetX: float = field(
        default=0.0,
        metadata={"description": "X-offset for Google Maps image alignment."},
    )
    GMoffsetY: float = field(
        default=0.0,
        metadata={"description": "Y-offset for Google Maps image alignment."},
    )
    lat_LL: float = field(
        default=0.0,
        metadata={"description": "Latitude at the lower-left corner of the map."},
    )
    lon_LL: float = field(
        default=0.0,
        metadata={"description": "Longitude at the lower-left corner of the map."},
    )
    lat_UR: float = field(
        default=0.0,
        metadata={"description": "Latitude at the upper-right corner of the map."},
    )
    lon_UR: float = field(
        default=0.0,
        metadata={"description": "Longitude at the upper-right corner of the map."},
    )

    # Simulation parameters
    render_step: int = field(
        default=1,
        metadata={
            "description": "Number of compute steps per render step. Higher values increase simulation speed but make visualization choppy."
        },
    )
    setRenderStep: int = field(
        default=0,
        metadata={
            "description": "Flag to automatically find the best render_step (0 = auto)."
        },
    )

    # Canvas interaction parameters
    xClick: int = field(
        default=0, metadata={"description": "Pixel X-coordinate of the canvas click."}
    )
    yClick: int = field(
        default=0, metadata={"description": "Pixel Y-coordinate of the canvas click."}
    )
    click_update: int = field(
        default=-1,
        metadata={
            "description": "Flag to indicate if the user clicked on the canvas (1 = clicked)."
        },
    )

    # Save data parameters
    write_eta: int = field(
        default=1,
        metadata={"description": "Flag to write eta surface data to file (1 = write)."},
    )
    write_P: int = field(
        default=0,
        metadata={
            "description": "Flag to write x flux surface data to file (1 = write)."
        },
    )
    write_Q: int = field(
        default=0,
        metadata={
            "description": "Flag to write y flux surface data to file (1 = write)."
        },
    )
    write_turb: int = field(
        default=0,
        metadata={
            "description": "Flag to write eddy viscosity surface data to file (1 = write)."
        },
    )
    dt_writesurface: float = field(
        default=1.0,
        metadata={"description": "Time increment for writing 2D surface data to file."},
    )
    fileWritePause: int = field(
        default=100,
        metadata={
            "description": "Pause duration (ms) during 2D surface writes to avoid buffer overload."
        },
    )
    write_individual_surface: int = field(
        default=0, metadata={"description": "Flag to write individual 2D surface data."}
    )
    which_surface_to_write: int = field(
        default=0, metadata={"description": "Identifier for which surface to write."}
    )

    # Time series and chart parameters
    n_time_steps_means: int = field(
        default=0,
        metadata={"description": "Counter for time steps used in means calculation."},
    )
    n_time_steps_waveheight: int = field(
        default=0,
        metadata={
            "description": "Counter for time steps used in wave height calculation."
        },
    )
    save_baseline: int = field(
        default=0,
        metadata={
            "description": "Flag to store baseline wave height texture (1 = store)."
        },
    )
    countTimeSeries: int = field(
        default=0, metadata={"description": "Counter for points stored in time series."}
    )
    durationTimeSeries: float = field(
        default=0.0, metadata={"description": "Current duration of the time series."}
    )
    maxdurationTimeSeries: float = field(
        default=120.0,
        metadata={
            "description": "Maximum duration of the time series before resetting."
        },
    )
    maxNumberOfTimeSeries: int = field(
        default=16, metadata={"description": "Maximum number of time series allowed."}
    )
    NumberOfTimeSeries: int = field(
        default=0, metadata={"description": "Current number of active time series."}
    )
    changethisTimeSeries: int = field(
        default=1,
        metadata={"description": "Identifier for the time series being changed."},
    )
    changeXTimeSeries: float = field(
        default=0.0,
        metadata={"description": "Updated X-coordinate of the time series."},
    )
    changeYTimeSeries: float = field(
        default=0.0,
        metadata={"description": "Updated Y-coordinate of the time series."},
    )
    updateTimeSeriesTx: int = field(
        default=0,
        metadata={
            "description": "Flag to update time series locations texture (1 = update)."
        },
    )
    locationOfTimeSeries: list = field(
        default_factory=lambda: [
            {"xts": 0.11744588732402632, "yts": 3.178500360934229},
            {"xts": 15.456250853855872, "yts": 3.3841330528485765},
            {"xts": 30.893381493250097, "yts": 2.6644186311483593},
            {"xts": 45.543906749745254, "yts": 2.4587859392340117},
            {"xts": 60.2927576791028, "yts": 2.0475205554053164},
            {"xts": 74.84495726273556, "yts": 2.9728676690198808},
            {"xts": 91.95362434079031, "yts": 2.6644186311483593},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
            {"xts": 0, "yts": 0},
        ],
        metadata={
            "description": "list of coordintes where the ts will be extracted from"
        },
    )

    # Tooltip values
    tooltipVal_eta: float = field(
        default=0.0, metadata={"description": "Tooltip value for eta surface."}
    )
    tooltipVal_bottom: float = field(
        default=0.0, metadata={"description": "Tooltip value for bottom surface."}
    )
    tooltipVal_Hs: float = field(
        default=0.0,
        metadata={"description": "Tooltip value for significant wave height."},
    )
    tooltipVal_friction: float = field(
        default=0.0, metadata={"description": "Tooltip value for friction."}
    )

    adapt_render_step: int = field(
        default=1, metadata={"description": "Whether to adapt the number of compute between renders to optimize performance"}
    )
    render_step: int = field(
        default=2, metadata={"description": "Number of compute steps between render (only matters if adapt_render_step=0)"}
    )


    zmin: int = field(
        default=-1, metadata={"description": "Min value of the bathymetry(<0) / topography (>0) array. Not used by Celeris."}
    )    

    zmax: int = field(
        default=-1, metadata={"description": "Max value of the bathymetry(<0) / topography (>0) array. Not used by Celeris."}
    )    
    trigger_writesurface: float = field(
        default=1, metadata={"description": "Flag to trigger writing surface output"}
    )  
    trigger_writesurface_start_time: float = field(
        default=0.0, metadata={"description": "Start time for writing surface output"}
    )
    trigger_writesurface_end_time: float = field(
        default=10000, metadata={"description": "End time for writing surface output"}
    )


import math
import random


@dataclass
class Wave:
    amplitude: float = field(
        metadata={
            "description": "wave amplitude measured measured from sealevel to the crest in meters"
        }
    )
    period: float = field(metadata={"description": "wave period in seconds"})
    direction: float = field(
        metadata={"description": "wave direction in radians, 0rad=East"}
    )
    phase: float = field(metadata={"description": "wave phase in radians"})


def write_waves(filename, waves):
    # Create waves
    with open(filename, "w") as file:
        file.write("\n")
        file.write(f"[NumberOfWaves] {len(waves)}\n")
        file.write("=================================\n")

        for wave in waves:
            cline = f"{wave.amplitude}\t{wave.period}\t{wave.direction}\t{wave.phase}"
            file.write(cline)
