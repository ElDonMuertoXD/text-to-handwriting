class FontConfig:
    """Configuration class for font-specific handwriting parameters"""
    
    def __init__(self):
        # Font settings
        self.font_size = 40
        self.line_height_offset = 20  # Added to font_size for line_height
        
        # Page layout
        self.margin_left = 100
        self.margin_top = 40
        self.margin_right = 80
        self.margin_bottom = 10
        self.page_width = 1240
        self.page_height = 1754
        
        # Character variation ranges
        self.character_variations = {
            'scale_x_range': (0.92, 1.08),
            'scale_y_range': (0.94, 1.06),
            'rotation_range': (-2.5, 2.5),  # degrees
            'baseline_offset_range': (-1.5, 1.5),
            'thickness_variation_range': (0.85, 1.15),
            'letter_spacing_range': (-2, 4),  # pixels
        }
        
        # Writing position variations
        self.position_variations = {
            'horizontal_variation_range': (-8, 8),
            'vertical_variation_range': (-7, 7),
            'character_x_variation_range': (-1.2, 1.2),
            'character_y_variation_range': (-0.8, 0.8),
            'line_spacing_variation_range': (-2, 3),
        }
        
        # Line tilt settings
        self.line_tilt = {
            'base_tilt_range': (-0.8, 0.8),
            'tilt_multiplier': 0.017453,  # Radians conversion factor
        }
        
        # Spacing settings
        self.spacing = {
            'space_width_base_multiplier': 0.3,  # font_size * this
            'space_width_variation_range': (-3, 6),
            'line_length_multiplier': 0.6,  # font_size * this for line calculations
        }
        
        # Fatigue effects
        self.fatigue = {
            'onset_factor': 0.7,  # Lines after this fraction show fatigue
            'spacing_variation_multiplier': 2,
            'tilt_variation_multiplier': 0.3,
            'size_variation_multiplier': 0.02,
            'tremor_intensity_multiplier': 0.5,
        }
        
        # Ink and color settings
        self.ink_colors = {
            'base_ink_color_ranges': {
                'r': (10, 30),
                'g': (10, 30),
                'b': (35, 65),
            }
        }
        
        # Surface roughness
        self.surface_roughness = {
            'roughness_chance': 0.4,  # 40% chance
            'roughness_offsets': [(-0.3, 0.2), (0.2, -0.3), (0.1, 0.4)],
            'rough_color_ranges': {
                'r': (180, 220),
                'g': (180, 220),
                'b': (200, 240),
            }
        }
        
        # Imperfections and artifacts
        self.imperfections = {
            'character_imperfection_chance': 0.15,
            'ink_blob_chance': 0.3,
            'blob_size_range': (1, 2),
            'ink_blob_color_ranges': {
                'r': (20, 40),
                'g': (20, 40),
                'b': (50, 80),
            },
            'artifact_chance': 0.08,  # 8% chance
            'artifact_position_variation': 3,
            'artifact_color_ranges': {
                'r': (40, 80),
                'g': (40, 80),
                'b': (60, 100),
            }
        }
        
        # Paper texture settings
        self.paper_texture = {
            'noise_intensity': 8,
            'tint_color': [252, 248, 240],
            'tint_blend_factor': 0.05,
            'texture_blend_factor': 0.95,
        }
        
        # Pencil margin settings
        self.pencil_margins = {
            'pencil_color': (168, 170, 173),
            'margin_offset': 25,  # Distance from text margin
            'tilt_variation_range': (-0.5, 0.5),
            'texture_color_offset': 5,
            'dot_color': (185, 188, 190),
            'dot_count': 3,
            'dot_spacing': 15,
            'dot_offset_from_margin': 35,
            'tick_color': (200, 202, 205),
            'tick_spacing_vertical': 120,
            'tick_spacing_horizontal': 180,
            'tick_size': 3,
        }
        
        # Post-processing effects
        self.post_processing = {
            'ink_bleeding': {
                'blur_radius': 0.5,
                'blend_factor': 0.15,
            },
            'phone_scan_distortion': {
                'top_offset_range': (5, 15),
                'bottom_offset_range': (-3, 3),
                'side_skew_range': (-5, 5),
                'corner_variation_range': (-5, 5),
            },
            'lighting': {
                'gradient_intensity': 15,
                'min_brightness': 240,
                'blend_factor': 0.05,
            },
            'scan_noise': {
                'noise_intensity': 2,
                'jpeg_quality': 92,
            }
        }
        
        # Background color
        self.background_color = (254, 252, 248)

def create_rumors_skill_config():
    """Create configuration optimized for RumorsSkill font"""
    config = FontConfig()
    
    # Adjust font settings for RumorsSkill characteristics
    config.font_size = 38  # Slightly reduced from 45
    config.line_height_offset = 28  # More line spacing
    
    # Adjust margins to give more space
    config.margin_left = 150
    config.margin_right = 160
    config.margin_top = 30
    config.margin_bottom = 20
    
    # Adjust character variations for this font style
    config.character_variations.update({
        'scale_x_range': (0.88, 1.12),  # More variation
        'scale_y_range': (0.90, 1.10),
        'rotation_range': (-2.5, 2.5),  # Reduced rotation to prevent overflow
        'baseline_offset_range': (-1.8, 1.8),  # Slightly reduced
        'thickness_variation_range': (0.85, 1.15),  # Reduced variation
        'letter_spacing_range': (-2, 3),  # Reduced max spacing
    })
    
    # Adjust spacing for this font - more conservative
    config.spacing.update({
        'space_width_base_multiplier': 0.32,  # Reduced from 0.35
        'space_width_variation_range': (-2, 4),  # Reduced variation
        'line_length_multiplier': 0.65,  # Increased for better calculations
    })
    
    # Adjust position variations to be more conservative
    config.position_variations.update({
        'horizontal_variation_range': (-5, 5),  # Reduced from (-8, 8)
        'vertical_variation_range': (-5, 5),    # Reduced from (-7, 7)
        'character_x_variation_range': (-0.8, 0.8),  # Reduced from (-1.2, 1.2)
        'character_y_variation_range': (-0.6, 0.6),  # Reduced from (-0.8, 0.8)
        'line_spacing_variation_range': (-1, 2),     # Reduced from (-2, 3)
    })
    
    return config

def create_brushy_handwriting_config():
    """Create configuration optimized for Brushy Handwriting font"""
    config = FontConfig()
    
    # Brushy fonts typically need more space and less variation
    config.font_size = 50
    config.line_height_offset = 32
    
    # More generous margins for brush-style writing
    config.margin_left = 100
    config.margin_right = 200
    config.margin_top = 100
    config.margin_bottom = 25
    
    # More variation for rougher appearance
    config.character_variations.update({
        'scale_x_range': (1.0, 1.05),  # Increased from (0.94, 1.06)
        'scale_y_range': (1.0, 1.05),  # Increased from (0.96, 1.04)
        'rotation_range': (-1.0, 1.0),  # Increased from (-1.5, 1.5)
        'baseline_offset_range': (-1.0, 1.0),  # Increased from (-1.0, 1.0)
        'thickness_variation_range': (0.80, 1.20),  # Increased from (0.90, 1.10)
        'letter_spacing_range': (-1, 1),  # Increased from (-1, 3)
    })
    
    # Conservative spacing for brush strokes
    config.spacing.update({
        'space_width_base_multiplier': 0.38,
        'space_width_variation_range': (-1, 1),  # Increased from (-1, 4)
        'line_length_multiplier': 0.68,
    })
    
    # More position variations for rougher look
    config.position_variations.update({
        'horizontal_variation_range': (-8, 8),  # Increased from (-4, 4)
        'vertical_variation_range': (-7, 7),    # Increased from (-4, 4)
        'character_x_variation_range': (-1.2, 1.2),  # Increased from (-0.6, 0.6)
        'character_y_variation_range': (-1.0, 1.0),  # Increased from (-0.5, 0.5)
        'line_spacing_variation_range': (-3, 4),     # Increased from (-1, 2)
    })
    
    # Darker ink colors
    config.ink_colors = {
        'base_ink_color_ranges': {
            'r': (5, 15),   # Darker - reduced from (10, 30)
            'g': (5, 15),   # Darker - reduced from (10, 30)
            'b': (15, 35),  # Darker - reduced from (35, 65)
        }
    }
    
    # Increase imperfections for rougher appearance
    config.imperfections.update({
        'character_imperfection_chance': 0.25,  # Increased from 0.15
        'ink_blob_chance': 0.45,  # Increased from 0.3
        'blob_size_range': (1, 3),  # Increased from (1, 2)
        'ink_blob_color_ranges': {
            'r': (10, 25),  # Darker blobs
            'g': (10, 25),
            'b': (25, 50),
        },
        'artifact_chance': 0.15,  # Increased from 0.08
        'artifact_position_variation': 5,  # Increased from 3
        'artifact_color_ranges': {
            'r': (20, 50),  # Darker artifacts
            'g': (20, 50),
            'b': (35, 70),
        }
    })
    
    # Increase surface roughness
    config.surface_roughness.update({
        'roughness_chance': 0.6,  # Increased from 0.4
        'roughness_offsets': [(-0.5, 0.3), (0.3, -0.5), (0.2, 0.6), (-0.4, -0.2)],  # More offsets
    })
    
    return config

def create_march_frost_config():
    """Create configuration optimized for March Frost font"""
    config = FontConfig()
    
    # March Frost is typically elegant and flowing
    config.font_size = 39
    config.line_height_offset = 30
    
    # Standard margins with slight adjustments
    config.margin_left = 130
    config.margin_right = 200
    config.margin_top = 50
    config.margin_bottom = 18
    
    # Elegant variations
    config.character_variations.update({
        'scale_x_range': (0.91, 1.09),
        'scale_y_range': (0.90, 1.10),
        'rotation_range': (-2.0, 2.0),
        'baseline_offset_range': (-1.5, 1.5),
        'thickness_variation_range': (0.87, 1.13),
        'letter_spacing_range': (-2, 4),
    })
    
    # Flowing spacing
    config.spacing.update({
        'space_width_base_multiplier': 0.33,
        'space_width_variation_range': (-2, 5),
        'line_length_multiplier': 0.63,
    })
    
    # Moderate variations for elegance
    config.position_variations.update({
        'horizontal_variation_range': (-7, 7),
        'vertical_variation_range': (-6, 6),
        'character_x_variation_range': (-0.9, 0.9),
        'character_y_variation_range': (-0.7, 0.7),
        'line_spacing_variation_range': (-2, 3),
    })
    
    return config

def create_rise_star_hand_config():
    """Create configuration optimized for RiseStarHand font"""
    config = FontConfig()
    
    # Light handwriting font, typically needs careful spacing
    config.font_size = 41
    config.line_height_offset = 24
    
    # Balanced margins
    config.margin_left = 125
    config.margin_right = 100
    config.margin_top = 100
    config.margin_bottom = 20
    
    # Light font variations
    config.character_variations.update({
        'scale_x_range': (0.89, 1.11),
        'scale_y_range': (0.91, 1.09),
        'rotation_range': (-2.8, 2.8),
        'baseline_offset_range': (-1.7, 1.7),
        'thickness_variation_range': (0.85, 1.15),
        'letter_spacing_range': (-2, 4),
    })
    
    # Standard spacing with slight adjustments
    config.spacing.update({
        'space_width_base_multiplier': 0.31,
        'space_width_variation_range': (-3, 5),
        'line_length_multiplier': 0.61,
    })
    
    # Natural handwriting variations
    config.position_variations.update({
        'horizontal_variation_range': (-7, 7),
        'vertical_variation_range': (-6, 6),
        'character_x_variation_range': (-1.1, 1.1),
        'character_y_variation_range': (-0.8, 0.8),
        'line_spacing_variation_range': (-2, 3),
    })
    
    return config

def create_sf_scribbled_sans_config():
    """Create configuration optimized for SF Scribbled Sans font"""
    config = FontConfig()
    
    # Scribbled fonts need more space and controlled variations
    config.font_size = 37
    config.line_height_offset = 30
    
    # Extra space for scribbled appearance
    config.margin_left = 120
    config.margin_right = 270
    config.margin_top = 100
    config.margin_bottom = 22
    
    # Scribbled variations - more controlled
    config.character_variations.update({
        'scale_x_range': (0.92, 1.08),
        'scale_y_range': (0.94, 1.06),
        'rotation_range': (-2.2, 2.2),
        'baseline_offset_range': (-1.3, 1.3),
        'thickness_variation_range': (0.88, 1.12),
        'letter_spacing_range': (-1, 4),
    })
    
    # Scribbled spacing
    config.spacing.update({
        'space_width_base_multiplier': 0.36,
        'space_width_variation_range': (-2, 6),
        'line_length_multiplier': 0.64,
    })
    
    # Controlled scribbled variations
    config.position_variations.update({
        'horizontal_variation_range': (-6, 6),
        'vertical_variation_range': (-5, 5),
        'character_x_variation_range': (-0.8, 0.8),
        'character_y_variation_range': (-0.6, 0.6),
        'line_spacing_variation_range': (-1, 2),
    })
    
    return config

# Font-specific configurations
FONT_CONFIGS = {
    'english_essay': FontConfig(),
    'rumors_skill': create_rumors_skill_config(),
    'brushy_handwriting': create_brushy_handwriting_config(),
    'march_frost': create_march_frost_config(),
    'rise_star_hand': create_rise_star_hand_config(),
    'sf_scribbled_sans': create_sf_scribbled_sans_config(),
    
    # You can add more font configs here by inheriting and modifying
    # 'default': create_default_config(),
}

def get_font_config(font_name):
    """Get configuration for a specific font"""
    return FONT_CONFIGS.get(font_name, FONT_CONFIGS['english_essay'])

def list_available_fonts():
    """List all available font configurations"""
    return list(FONT_CONFIGS.keys())