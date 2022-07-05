(define pp-inessive-location-phrase-input
  (def-contextual-space :name "pp[location-phrase].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define pp-inessive-location-phrase-output
  (def-contextual-space :name "pp[location-phrase].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define pp-inessive-location-phrase
  (def-frame :name "pp[location-phrase]"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space pp-inessive-location-phrase-input
    :output_space pp-inessive-location-phrase-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) pp-inessive-location-phrase-input))
    :parent_space pp-inessive-location-phrase-input))
(define chunk-location-label
  (def-label :start chunk :parent_concept everywhere-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-phrase-input))
    :parent_space pp-inessive-location-phrase-input))

(define pp-word
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-phrase-output))
    :parent_space pp-inessive-location-phrase-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) pp-inessive-location-phrase-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word :parent_concept everywhere-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-phrase-output))))

(def-relation :start label-concept :end pp-inessive-location-phrase
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-inessive-location-phrase
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-inessive-location-phrase
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-inessive-location-phrase
  :is_bidirectional True :activation 1.0)
