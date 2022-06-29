(define pp-inessive-time-input
  (def-contextual-space :name "pp[time-phrase].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define pp-inessive-time-output
  (def-contextual-space :name "pp[time-phrase].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define pp-inessive-time
  (def-frame :name "pp[time-phrase]"
    :parent_concept pp-inessive-time-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space pp-inessive-time-input
    :output_space pp-inessive-time-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) time-space)
			      (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))
(define chunk-time-label
  (def-label :start chunk :parent_concept everywhere-concept
    :locations (list (Location (list (list Nan Nan)) time-space)
		     (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))

(define pp-word
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list (list Nan Nan)) time-space)
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) pp-inessive-time-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word :parent_concept everywhere-concept
    :locations (list (Location (list (list Nan Nan)) time-space)
		     (Location (list) pp-inessive-time-output))))

(def-relation :start label-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
