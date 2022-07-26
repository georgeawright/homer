(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureCollection temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list) conceptual-space))))

(define ap-sub-frame-input
  (def-contextual-space :name "ap-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define ap-sub-frame
  (def-sub-frame :name "s[ap-in-loc-on-day]-ap-sub"
    :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection label-parent-concept)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))

(define loc-sub-frame-input
  (def-contextual-space :name "loc-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define loc-sub-frame-output
  (def-contextual-space :name "loc-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define loc-sub-frame
  (def-sub-frame :name "s[ap-in-loc-on-day]-loc-sub"
    :parent_concept pp-inessive-location-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-concept)
    :input_space loc-sub-frame-input
    :output_space loc-sub-frame-output))

(define day-sub-frame-input
  (def-contextual-space :name "day-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define day-sub-frame-output
  (def-contextual-space :name "day-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define day-sub-frame
  (def-sub-frame :name "s[ap-in-loc-on-day]-day-sub"
    :parent_concept pp-inessive-time-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection time-concept)
    :input_space day-sub-frame-input
    :output_space day-sub-frame-output))

(define descriptive-sentence-input
  (def-contextual-space :name "s[ap-in-loc-on-day].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space conceptual-space)))
(define descriptive-sentence-output
  (def-contextual-space :name "s[ap-in-loc-on-day].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space time-space conceptual-space)))
(define descriptive-sentence
  (def-frame :name "s[ap-in-loc-on-day]"
    :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection ap-sub-frame loc-sub-frame day-sub-frame)
    :concepts (StructureCollection label-parent-concept location-concept time-concept)
    :input_space descriptive-sentence-input
    :output_space descriptive-sentence-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) conceptual-space)
			      (Location (list) ap-sub-frame-input)
			      (Location (list) loc-sub-frame-input)
			      (Location (list) day-sub-frame-input)
			      (Location (list) descriptive-sentence-input))
    :parent_space loc-sub-frame-input))
(define chunk-location-label
  (def-label :start chunk :parent_concept location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) loc-sub-frame-input)
		     (Location (list) descriptive-sentence-input))
    :parent_space loc-sub-frame-input))
(define chunk-time-label
  (def-label :start chunk :parent_concept time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) day-sub-frame-input)
		     (Location (list) descriptive-sentence-input))
    :parent_space day-sub-frame-input))
(define chunk-conceptual-label
  (def-label :start chunk :parent_concept label-parent-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) ap-sub-frame-input)
		     (Location (list) descriptive-sentence-input))
    :parent_space ap-sub-frame-input))
(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) descriptive-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "be"
    :locations (list cop-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :abstract_chunk be))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) descriptive-sentence-output))
    :parent_space ap-sub-frame-output))
(define sentence-word-4-grammar-label
  (def-label :start sentence-word-4 :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) loc-sub-frame-output)
		     (Location (list) descriptive-sentence-output))
    :parent_space loc-sub-frame-output))
(define sentence-word-5-grammar-label
   (def-label :start sentence-word-5 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) loc-sub-frame-output))))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) day-sub-frame-output)
		     (Location (list) descriptive-sentence-output))
    :parent_space day-sub-frame-output))
(define sentence-word-6-grammar-label
   (def-label :start sentence-word-6 :parent_concept pp-inessive-time-concept
    :locations (list pp-location
		     (Location (list) day-sub-frame-output))))

(define vb-super-chunk
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :left_branch (StructureCollection sentence-word-2)
    :right_branch (StructureCollection sentence-word-3)))
(define vb-super-chunk-label
  (def-label :start vb-super-chunk :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) descriptive-sentence-output))))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :left_branch (StructureCollection sentence-word-5)
    :right_branch (StructureCollection sentence-word-6)))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :left_branch (StructureCollection sentence-word-4)
    :right_branch (StructureCollection pp-super-chunk)))
(define pred-super-chunk-label
   (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) descriptive-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :left_branch (StructureCollection vb-super-chunk)
    :right_branch (StructureCollection pred-super-chunk)))
(define vp-super-chunk-label
   (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) descriptive-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) descriptive-sentence-output))
    :parent_space descriptive-sentence-output
    :left_branch (StructureCollection sentence-word-1)
    :right_branch (StructureCollection vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) descriptive-sentence-output))))

(def-relation :start label-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start nn-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jj-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end descriptive-sentence
  :is_bidirectional True :activation 1.0)
